import tensorflow
import tensorflow_hub as hub
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
import gensim
from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_multiple_whitespaces

from operator import itemgetter
import sqlite3
import pandas as pd

import sys

np.set_printoptions(threshold=sys.maxsize)

module_url = "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("/home/suraj/Downloads/suraj_k_liye.sqlite")
df = pd.read_sql_query("SELECT * from Article", con)

# Verify that result of SQL query is stored in the dataframe
print(df)
#df=df[df['content']==""]
#print(type(df['content'].notna()))
print("-----------------------")
df=df.iloc[df['content'].notna().tolist()]
print(len(df))
df=df.iloc[df['content'].notnull().tolist()]
print(len(df))
df=df.drop(df[df['content'] == ''].index)
print(len(df))
df=df[~ df['content'].duplicated()]
print(df)
print(len(df))
print("-----------------------")

links=df['url'].tolist()
messages=df['content'].tolist()
stop_words_removed=[]
for message in messages:
    message = strip_punctuation(message)
    message = strip_multiple_whitespaces(message)
    stop_words_removed.append(remove_stopwords(message))
    #print(remove_stopwords(message))
print(len(messages))

def heatmap(x_labels, y_labels, values):
    fig, ax = plt.subplots()
    im = ax.imshow(values)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10,
         rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, "%.2f"%values[i, j],
                           ha="center", va="center", color="w", fontsize=6)

    fig.tight_layout()
    plt.show()

# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)

# sample text
messages = [
#Tcs
    """
    
    However, shares of Tata Communications, Tata Consultancy Services (TCS) and Tata Elxsi traded in the red.

    Tata Sons board is set to meet later in the day to take stock of the coronavirus situation and assess the impact on individual companies, CNBC-TV18 reported sources as saying.
    With many states unlocking, it is important to discuss operations across group companies and the plan of action for states that are undergoing more lockdowns.

    Another key point will fund infusion into group companies after assessing the requirements, said sources. The two companies to keep a close watch on are Tata Steel and JLR, the report said.

    The board will also assess the debt-reduction plan for companies as it wants to deleverage and reduce risks across the group. A long-term strategy for businesses like aviation, consumer, and IT may also be on the agenda.

    The group may also look to fast track merger of businesses with a similar business focus, something that has been on the agenda for a while. Reports have also indicated that Tata Sons was the only company in the race for Air India assets. The bidding strategy may also be on the agenda, CNBC-TV18 reported.
    The meeting comes a month after the board met in June to assess the performance of the group companies. 
    """ , 
    """ Shares of Tata Group firms such as Tata Steel, Tata Motors, Tata Consumer and Tata Power Company were trading higher on BSE in the afternoon on July 17 ahead of the group's meet.

        
        However, shares of Tata Communications, Tata Consultancy Services (TCS) and Tata Elxsi traded in the red.

        Tata Sons board is set to meet later in the day to take stock of the coronavirus situation and assess the impact on individual companies, CNBC-TV18 reported sources as saying.

        With many states unlocking, it is important to discuss operations across group companies and the plan of action for states that are undergoing more lockdowns.
    """,
    """ 
        
        However, shares of Tata Communications, Tata Consultancy Services (TCS) and Tata Elxsi traded in the red.

        Tata Sons board is set to meet later in the day to take stock of the coronavirus situation and assess the impact on individual companies, CNBC-TV18 reported sources as saying.

        With many states unlocking, it is important to discuss operations across group companies and the plan of action for states that are undergoing more lockdowns.

        Another key point will fund infusion into group companies after assessing the requirements, said sources. The two companies to keep a close watch on are Tata Steel and JLR, the report said.

        The board will also assess the debt-reduction plan for companies as it wants to deleverage and reduce risks across the group. A long-term strategy for businesses like aviation, consumer, and IT may also be on the agenda.

        The group may also look to fast track merger of businesses with a similar business focus, something that has been on the agenda for a while. Reports have also indicated that Tata Sons was the only company in the race for Air India assets. The bidding strategy may also be on the agenda, CNBC-TV18 reported.

        The meeting comes a month after the board met in June to assess the performance of the group compani
    """,
#Yes bank
    """YES Bank’s further public offer was subscribed 0.48 times on Day 2 even as qualified institutional buyers subscribed fully. The private sector lender’s scrip closed 5.87 per cent lower at ₹19.25 on the BSE on Thursday. According to data from exchanges, the ₹15,000-crore FPO received bids for 434.15 crore shares as against 909.97 crore shares on offer. The QIB portion has been oversubscribed 1.19 times while HNIs portion 0.11 times. Retail investors have subscribed 0.20 times and employee portion has received just 0.11 times. The share sale ends on July 17. 
    """ ,
    """ The further public offering of private sector lender Yes Bank has been subscribed 47.94 percent so far on the second day of bidding - July 16.

        The public issue has received bids for more than 434.15 crore equity shares against offer size of over 909.97 crore shares (excluding anchor book portion), the data available on exchanges showed.

        The portion set aside for qualified institutional buyers fully subscribed and that of non-institutional investors 10.8 percent, while the reserved portion of retail investors was subscribed 19.3 percent and employees' portion at  10.6 percent.

        The private sector lender intends to raise Rs 15,000 crore through its FPO which is scheduled to close on July 17. The price band for FPO has been fixed at Rs 12-13 per share, a major discount to market price.

        The follow-on offer is available at a deep discount to the current market price, without lock-in period criteria, which makes it a unique investment opportunity, said KR Choksey while advising subscribe rating.

        While we see elevated stress pockets for the bank, we draw comfort from the backing of SBI as a key stakeholder (48.2 percent stake in Yes Bank as of June 2020 and lock-in period of 3 years) to absorb any shock," said the brokerage, adding the key investment risk remains the expected stress on its balance sheet; both from the lending portfolio and the investment book.

        Apart from SBI, Yes Bank has also been supported by other marquee institutions – Kotak Mahindra Bank, ICICI Bank, Federal Bank, HDFC, Axis Bank, Bandhan Bank and IDFC First Bank which all including SBI had invested Rs 10,000 crore in the bank through Reconstruction Scheme in March this year.

        Given the COVID-19 fallout, KR Choksey expects more stress emerging for the bank in the near future, but considering the remedial measures undertaken by RBI/GoI (moratorium window) the actual NPA formation is expected to be deferred by a quarter or two.

        The FPO is largely aimed to ensure adequate capital buffer to support growth plans, alongside absorbing further stress points from high NPA levels.

        As of March 31, 2020, its common equity tier I ratio (a measure of bank solvency) was at 6.3 percent, which was lower than the RBI's minimum CET I ratio of 7.375 percent.

        Yes Bank, which is in need of liquidity and that is a reason behind this FPO launch, has already garnered Rs 4,098 crore by issuing more than 341.53 crore equity shares at Rs 12 per share, to 12 anchor investors including Bay Tree India Holdings I LLC, HDFC Life Insurance Company, Amansa Holdings, Elara India Opportunities, Jupiter India Fund, ICICI Lombard General etc.

        Bids can be made for minimum 1,000 shares and in multiples of 1,000 shares thereafter.
        Kotak Mahindra Capital Company, SBI Capital Markets, Axis Capital, Citigroup Global Markets India, DSP Merrill Lynch, HSBC Securities and Capital Markets (India), ICICI Securities and Yes Securities India are the book running lead managers to the issue. 
    """ ,
    """ The follow-on public offer (FPO) of YES Bank on Friday has been overall subscribed 95 percent at Rs 14,266.97 crore. The total size of YES Bank FPO is Rs 15,000 crore.

        A total of 27 institutions bid for the QIB portion such as SBI, LIC, IIFL, Edelweiss, Bajaj Allianz, HDFC Life, Punjab National Bank, HDFC MF, Union Bank, Bajaj Holdings, Avendus Wealth Management, IFFCO Tokio General Insurance, Norges fund, Schonfled, Millennium Management Global, Aurigin Capital, Exodus Capital, Wellington Capital, Jane StreetCapital, Segantii Capital Management and De Shaw & Co.

        On its final day, the QIB portion was subscribed 1.90 times, non-institutional investor portion was subscribed 0.63 times, retail portion was subscribed 0.47 times and employee portion was subscribed 0.33 times.

        The maximum bids has been received at lower end of price band of Rs 12-13 per share. The anchor book, through which the lender has received Rs 4,098 crore, has also been subscribed at Rs 12 per share.

        Prashant Kumar, managing director and chief executive officer, YES BANK said, "We are pleased with the completion of our further public offering and would like to thank all the investors, partners and employees who have supported the issue. It is an important step in our journey of transformation and is a testament to the trust placed in the institution."
        On July  14, the bank had raised Rs 4,098 crore from 14 anchors at Rs 12 per share to US- based alternative asset manager, Tilden Park Capital via BayTree India Holdings LLC; Singapore-based fund management company, Amansa Capital and UK-based Fund management company, Jupiter Funds, collectively these 3 FPIs came together to acquire 75 of the shares offered to the anchors. 
    """ ,
    #jio
    """ Reliance Jio Infocomm Ltd is in favour of rationalizing the huge differences between standard rates and pack tariffs offered under international mobile roaming (IMR) services, but Bharti Airtel and Vodafone Idea Ltd think the otherwise as it may impact the interest of consumers. This could be seen as another point of contention in the bitter tariff war going among the three telcos since the launch of Mukesh Ambani-led Jio in 2016.

        The Telecom Regulatory Authority of India (Trai) in May had floated a consultation paper on ‘Regulation of International Mobile Roaming Services’, pointing at the significant divergence between standard rates and pack tariffs, among several other issues that lead to bill shocks to consumers on international roaming.

        For instance, telcos offer standard rate of ₹90 per minute for incoming calls while roaming in the US and calls to India cost ₹180 per minute. But one-day pack with unlimited incoming calls and 100 minutes of calls to India is being offered at ₹575, Trai said in its paper, which was for open to comments from stakeholders till 7 July.

        Even a cursory glance of tariff offerings of all the TSPs (telecom service providers) show that standard rates are significantly higher than the rates offered under the IR (international roaming) packs,” Trai added.

        However, all three telcos recommended that international roaming charges should not be regulated and any intervention by Trai may limit the scope of improvement in these services given the complex structure of such tariffs involving deals and negotiations with many foreign operators.

        Trai should focus on proactive information and consumer awareness instead of restricting voluntary usage of IMR. “We submit that the flexibility of designing tariff plans should be left to market forces while selection of a suitable plan should be left at discretion of the consumer,” Jio said in its reply to the consultation paper.

        As far as the difference in standard rates and pack tariffs is concerned, Vodafone Idea said it has a strong “economic/commercial rationale to merit such a distinction” as the services are provided to various segments of consumers.

        In US, only we have proportion of 65 of postpaid customers who are actually roaming on IR packs and 35 on standard rates. In case of prepaid customers, out of actual roamers, 80 are on standard rates and only 20 are on IR packs, Vodafone Idea said.

        Bharti Airtel said, to protect its consumers from standard rates, it has ‘Roam Without Fear’ plan that prevents accidental usage of data by barring consumers from using the service beyond their daily pack limit.

        In our view, rationalization of standard rates doesn’t impact the as they are already protected with the measures undertaken by us,” Airtel said in its comments.

        The tel cos also said they are already following various other measures mentioned in the consultation paper including communicating all details of activation and applicable tariff immediately by SMS (short message service) or e-mail once a plan is selected by a subscriber, and regulatory intervention may not be required in this case.
    """
    #LG
    """ LG Electronics has been reportedly hit by a Maze ransomware attack. The report states that Maze ransomware operators claim to have breached and locked LG Electronics' network. The hackers claim they have stolen proprietary information for projects that involve big US companies and one of them seems to be AT&T. As of now, it is unclear how the Maze ransomware operators hacked into LG's network and what their demands are. The attackers have shared some screenshots of stolen data from a Python code repository.

        Maze ransomware was first discovered in 2019. The goal of this ransomware, according to McAfee's blog, is to encrypt files on a system blocking access to them and releasing this block when the ransom has been paid or the demands have been met. Its operators can also send the data back to the hackers who can then release the data to the public, or sell it if the ransom is not paid.

        As per the report by Bleeping Computer, LG Electronics seems to have been attacked by Maze ransomware. The attackers posted a few screenshots of the data they stole, stating that they were able to steal 40GB of Python code that LG developed for large companies in the US. One of the screenshots shared by the hackers shows a split archive for a .KDZ file which is said to be the official stock firmware code from LG, as per the report. The attack seems to have taken place on or before June 22 as that is when the hackers put out a press release stating that they will soon reveal how LG company's source code was stolen that belonged to “one very big telecommunications company, working worldwide”.

        This  telecommunication company they are referring to could be AT&T, an American multinational conglomerate holding company and one of the world's largest telecommunication companies. The Maze ransomware operators shared three screenshots on their website, one of which shows several files with “xxx_00_ATT_US_OP_xxx” name. This suggests that the firmware was developed for AT&T. The report also states that 41 LG phones and four tablets are listed on AT&T's support page.

        It is unclear how the Maze ransomware operators got access to the data and what their demands are. Gadgets 360 reached out to LG for clarity, and received the following statement as a response: "At LG we take cybersecurity issues very seriously and are looking into this alleged incident. If necessary, we will involve appropriate law enforcement agencies if there is evidence that a crime has been committed but to date, we have not received any communication from anyone regarding this supposed theft."
    """ ,
    """ The operators of Maze ransomware claim to have breached its biggest victim yet, LG Electronics, which indicates a troubling trend for large enterprises.

        As proof of the breach, Maze released three screenshots. One of the screenshots appears to consist of LG Electronics official firmware or software update releases that assist their hardware, according to a blog post by Cyble, a cyber threat intelligence company.

        Another screenshot lists LG product source code, which was promised by Maze in their June 22 press release teasing the breach. The release was in large part a warning from the ransomware operators to victims regarding "the cost of non-cooperation." In other words, if a company doesn't pay up to Maze, there will be consequences.

        Though some enterprises of note have been known victims of Maze, like Pitney Bowes and Cognizant, no known victim has come close in size to LG, which had a 2018 revenue of $54.398 billion. In Pitney Bowes' case, while hackers did breach and access data, they were stopped before the ransomware detonated. While most of Maze's victims consist of smaller organizations, LG's compromise (not to mention Pitney Bowes' and Cognizant's) indicates a trend that Maze's victims are getting larger and larger.
    """ ,
    """ South Korea's LG Electronics has been hit by a ransomware attack carried out by the Maze hacker group, which appears to have stolen proprietary information for projects linked to large US companies. 

        The group initially said in a message posted last week that it would provide information on the alleged breach of LG including source code it had stolen. Several days later, Maze claimed it stole 40 gigabytes of python source codes developed for companies in the US, and posted a number of screenshots showing files and codes. The hackers did not specify the ransom they had demanded from LG.

        According to Forbes, if such codes for electronic devices wind up in the wrong hands, they might be used to develop highly-targeted exploits that could be utilized to deliver surveillance tools, ransomware and cryptominers. 

        It was not immediately known how Maze breached the company's network. In previous attacks, the actor is said to have infiltrated via vulnerabilities in public internet systems, exposed remote desktops or compromised administrator accounts.

        Maze's modus operandi is to infiltrate a network, often obtaining information from other hacking groups, and then boost its privileges to gain wider access. It has a reputation of publishing stolen files if their victims don't agree to pay ransom.  Reports said the Maze group has hacked a number of enterprises recently but never one that is the size of the multinational company.  
    """ ,
    """ LG Electronics was allegedly hit by Maze Ransomware who leaked screenshots of some of the files they claim to have stolen. Unfortunately, LG has not responded to any of our emails to confirm the details.
    """ ,
    #something else
    """ BENGALURU: The Bosch India plant at Bidadi in Ramanagara has 62 Covid-positive cases of the 768 employees tested, stated an internal email, of which TNIE has a copy. The communication, dated July 2, states that one patient has recovered, while 182 primary contacts have been quarantined. The testing has started in phases and will cover all employees. District Health Officer Dr Niranjan, however, said there are only 48 cases at the plant. “The unit has to be sealed until the premises are sanitised. Positive patients have been admitted in Bengaluru and we are conducting primary and secondary contact tracing in Ramanagara,” he said.
        Bosch’s Bidadi plant hit by 62 Covid-19 cases
        Bosch workers at Karnataka's Bidadi plant tense after eight contract COVID-19
    """ ,
    """ BENGALURU: The fears that Unlock 1.0 brought with it are playing out at Bosch’s Bidadi plant, where eight workers tested positive for the coronavirus through this week. Workers at the plant are afraid to come to work, and want the management to disinfect the factory and seal it for a few days. However, the management is not inclined to shut down the factory, fuelling their anxiety.

        “The management has not given us official confirmation on workers testing positive, but we heard about it. When there are positive cases in an area, a portion is sealed down but no such thing has happened here. It is a risk for us,” said a factory worker, on condition of anonymity. The automobile plant has four duty shifts. The workers’ union has been asking for leave but the management has not agreed so far. Workers are also scared to complain or raise the issue.”
    """
]
print(len(messages))
stop_words_removed=[]
for message in messages:
    message = strip_punctuation(message)
    message = strip_multiple_whitespaces(message)
    stop_words_removed.append(remove_stopwords(message))
print("-------------------------------------")
similarity_input_placeholder = tensorflow.placeholder(tensorflow.string, shape=(None))
similarity_message_encodings = embed(similarity_input_placeholder)
corr=None
with tensorflow.Session() as session:
    session.run(tensorflow.global_variables_initializer())
    session.run(tensorflow.tables_initializer())
    message_embeddings_ = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: stop_words_removed})
    print(message_embeddings_.shape)
    print(type(message_embeddings_))
    corr = np.inner(message_embeddings_, message_embeddings_)
    print(corr)
    #heatmap(messages, messages, corr)
#print(corr.shape)
#print(np.where(corr[0]>0.8))
threshold=0.75
print(np.where(corr[0]>threshold)[0].tolist())

#print(messages[np.where(corr[0]>0.8)[0].tolist()])
print(len(messages))
print("############################################################################################################################")
already_checked=[]
with open("output.txt", "w") as file1:
    file1.write("##########################################----Testing New article-----####################################################"+"\n")
    for i in range(len(messages)):
        print("!----!")
        print(np.where(corr[i]>threshold))
        #print("already_checked:",already_checked)
        #print("check:",np.where(corr[i]>threshold)[0].tolist())
        if len(np.where(corr[i]>threshold)[0].tolist())>1:
            print("----------------------All articles Below match with each other-------------------")
            file1.write("----------------------All articles Below match with each other-------------------"+"\n")
            for n,m in zip(np.where(corr[i]>threshold)[0].tolist(),itemgetter(*np.where(corr[i]>threshold)[0].tolist())(messages)):
                #print(n)
                if not (np.where(corr[i]>threshold)[0].tolist() in already_checked ):
                    print("link of the below article :",links[n])
                    file1.write("link of the below article :"+links[n]+"\n")
                    print(m)
                    file1.write(m+"\n")
                    print("--------new matching article---------")
                    file1.write("--------new matching article---------"+"\n")

                else:
                    #print("already checked this article")
                    break
            already_checked.append(np.where(corr[i]>threshold)[0].tolist())
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!1!no match for this article!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            file1.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!no match for this article!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"+"\n")
            print("link of the below article :",links[n])
            file1.write("link of the below article :"+links[n]+"\n")
            loc=np.where(corr[i]>threshold)[0].tolist()[0]
            print(messages[loc])
            file1.write(messages[loc]+"\n")
        print("################################################----Testing New article-----###################################################")
        file1.write("##########################################----Testing New article-----####################################################"+"\n")
        
#print(itemgetter(*np.where(corr[0]>0.8)[0].tolist())(messages))
