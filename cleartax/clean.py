

import json
import re


def clean_text(text):
    # Remove text from 'For any clarifications/feedback on the topic' until the end of the sentence
    text = re.sub(
        r'For any clarifications/feedback on the topic[^.!?]*[.!?]', '', text, flags=re.IGNORECASE | re.DOTALL)

    # Remove text after 'Read More' until the next '\n' or end of sentence
    text = re.sub(r'Read More.*?(\n|$)', '', text,
                  flags=re.IGNORECASE | re.DOTALL)

    # Remove text after 'Also Read' until the next '\n' or end of sentence
    text = re.sub(r'Also Read.*?(\n|$)', '', text,
                  flags=re.IGNORECASE | re.DOTALL)

    # Replace multiple \n with a single \n
    text = re.sub(r'\n+', '\n', text)

    return text


# with open('conversation.json', 'r') as file, open('conversation_clean.json', 'w') as write_file:
#     data = json.load(file)
#     substrings_to_remove = ["Also Read", "For any clarifications"]
#     clean_data = []

#     for d in data:
#         d['conversations'][0]['value'] = d['conversations'][0]['value'].replace(
#             '\\', '').replace('\"', '')
#         d['conversations'][1]['value'] = clean_text(
#             d['conversations'][1]['value'])
#         clean_data.append(d)

#     json.dump(clean_data, write_file, ensure_ascii=False, indent=4)


def clean_text(text: str):
    print(text)
    print('----')
    # Remove text from 'For any clarifications/feedback on the topic' until the end of the sentence
    cl = text.find('For any clarifications/feedback on the topic')
    if cl != -1:
        text = text[:cl]

    text = text.replace('Also Read:', '\n')
    # Replace multiple \n with a single \n
    text = re.sub(r'\n+', '\n', text)

    return text


# Example text
input_text = "Do you want to diversify your equity portfolio with mid-cap and small-cap stocks? Are you looking for a mutual fund to create wealth in the long term? You may consider putting money in flexi-cap funds. It invests a minimum of 65% of the total assets in equity and equity-related instruments. You may find flexi-cap funds investing across large-cap, mid-cap and small-cap stocks. It offers mutual fund managers the freedom to put money in stocks across market capitalisation, to generate returns for investors over some time. However, should you invest in flexi-cap funds?\nWhat are Flexi-cap Funds?\nSecurities and Exchange Board of India (SEBI), passed a circular on November 09, 2020, announcing a new category of equity funds called flexi-cap funds. It is an equity-diversified mutual fund that invests in stocks across market capitalisation. \nThe fund manager selects stocks across different sectors and market capitalisation depending on the mutual fund’s investment objectives. The asset management companies would choose a suitable benchmark index to gauge the performance of flexi-cap funds. \nWhy did SEBI create a new category called flexi-cap funds?\nMulti-cap funds invest a minimum of 65% of the total assets in equity and equity-related securities. The multi-cap mutual fund scheme’s fund manager may pick stocks of companies in different sectors and industries across market-capitalisation. However, you would find the fund manager investing most of the multi-cap fund assets in large-cap stocks.\nYou would find many investors putting money in multi-cap funds. It emerged as the largest category of equity funds with assets under management (AUM) of Rs 1.13 lakh crore as of March 31, 2020. \nSEBI wanted multi-cap funds to stay true-to-label and put money in stocks of various sectors and industries across market capitalisation. It passed a rule on September 11, 2020, where multi-cap funds had to invest a minimum of 75% of total assets in equity and equity-related instruments. Multi-cap funds also had to maintain a minimum allocation of 25% each, towards large-cap, mid-cap and small-cap stocks. \nMutual funds had to comply with these rules by January 31, 2020. However, several AMCs and fund managers opposed the new rule as multi-cap funds invested heavily in large-cap stocks. It would be difficult to liquidate large-cap positions and invest significant amounts in mid-cap and small-cap stocks to adhere to the market capitalisation requirements, without significantly impacting prices. Mutual fund managers wanted SEBI to reconsider the rules on multi-cap funds. \nSEBI created a new category of equity funds called flexi-cap funds, rather than review the rules for multi-cap funds. It allows fund managers to invest in stocks of companies in different sectors across market capitalisation. Moreover, flexi-cap funds had to put a minimum of 65% of total assets in equity and equity-related securities. \nAlso Read: What You Should Know About Home Insurance in India?\nYou would find many AMCs recategorising multi-cap funds as flexi-cap, to retain their existing portfolios. It allows fund managers to invest in large-cap, mid-cap and small-cap stocks based on opportunities in the market, to generate a higher return. However, you may find flexi-cap funds continuing to invest a major portion of the assets in large-cap stocks. \nShould you invest in flexi-cap funds?\nYou may consider investing in flexi-cap funds only if it matches your investment objectives and risk tolerance. Flexi-cap funds could invest in mid-cap and small-cap stocks. You may put money in these funds if you are an aggressive investor with an investment horizon of over five years. \nYou may find flexi-cap funds investing heavily in large-cap stocks for some time. The fund manager may shift assets to mid-cap and small-cap stocks depending on investment opportunities. However, you could find fund managers sticking to large-cap stocks in the current scenario, owing to a dearth of small businesses’ quality investments. You could invest in large-cap funds instead of flexi-cap funds if you prefer putting money in large companies’ stocks. \nYou may find several mutual fund houses recategorising multi-cap schemes as flexi-cap to adhere to SEBI’s new rules. You may stay with your investment as AMCs have only changed the scheme’s name and the category. You would find the flexi-cap scheme maintaining the same investment objectives, portfolio allocation and the team to manage the fund. \nIf you have invested in multi-cap funds, you have a mandatory 30-day window to redeem the mutual fund units without any exit load. You won’t incur short-term or long-term capital gains tax depending on the holding period if your multi-cap fund has been recategorised as a flexi-cap fund. However, if you redeem units, the sale proceeds are subject to capital gains tax. \nYou could check the fund house’s track record and the fund manager’s investment style over three to five years. You may continue with your investment if you are happy with the fund house’s performance and the mutual fund manager. However, you may exit the flexi-cap fund if it has underperformed compared to peers over some time. \nFor any clarifications/feedback on the topic, please contact the writer at cleyon.dsouza@cleartax.in\nI write to make complicated financial topics, simple. Writing is my passion and I believe if you find the right words, it’s simple."

cleaned_text = clean_text(input_text)
print(cleaned_text)
