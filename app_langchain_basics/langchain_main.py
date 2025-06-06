"""
Main class for playground
"""

from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from app.constants.config import ModelDetails
from app.constants.templates import Templates

information = """
Cristiano Ronaldo dos Santos Aveiro (Portuguese pronunciation: [kɾiʃˈtjɐnu ʁɔˈnaldu] ⓘ; born 5 February 1985) is a Portuguese professional footballer who plays as a forward for and captains both Saudi Pro League club Al-Nassr and the Portugal national team. Nicknamed CR7, he is widely regarded as one of the greatest players of all time, and has won numerous individual accolades throughout his professional footballing career, including five Ballon d'Or awards, a record three UEFA Men's Player of the Year Awards, four European Golden Shoes, and was named five times the world's best player by FIFA.[note 3] He has won 33 trophies in his career, including seven league titles, five UEFA Champions Leagues and the UEFA European Championship. Ronaldo holds the records for most goals (140) and assists (42) in the Champions League, goals (14) and assists (8) in the European Championship, and most international appearances (220) and international goals (137). He is one of the few players to have made over 1,200 professional career appearances, the most by an outfield player, and has scored over 900 official senior career goals for club and country, making him the top goalscorer of all time.[note 4]
Ronaldo began his senior career with Sporting CP, before signing with Manchester United in 2003, winning the FA Cup in his first season. He went on to become a star player at United, as they won three consecutive Premier League titles, the Champions League and the FIFA Club World Cup; his 2007–08 season earned him his first Ballon d'Or, aged 23. Ronaldo was the subject of the then-most expensive association football transfer when he signed for Real Madrid in 2009 in a transfer worth €94 million (£80 million). He was integral to Madrid becoming a dominant force again, as they won four Champions Leagues from 2014 to 2018, including La Décima. He won back-to-back Ballon d'Or awards in 2013 and 2014, and again in 2016 and 2017, and was runner-up three times behind Lionel Messi, his perceived career rival. He also became the club's all-time top goalscorer and finished as the Champions League's top scorer for six consecutive seasons between 2012 and 2018. With Madrid, Ronaldo's additional titles include two La Liga titles, including a record-breaking title win in 2011-12, and two Copas del Rey. In 2018, following issues with the Madrid hierarchy, Ronaldo made a surprise transfer to Juventus in a transfer worth an initial €100 million (£88 million). He won several trophies in Italy, including two Serie A titles and a Coppa Italia, and broke several records for Juventus. He returned to United in 2021; despite a collectively disappointing season, Ronaldo's individual performances earned him being included in the PFA Team of the Year at 37 years old. His contract was terminated in 2022 due to a fall out with the newly appointed manager, and in 2023 he signed for Al-Nassr, a move that has since been widely credited for revolutionising football in Saudi Arabia.
Ronaldo made his international debut for Portugal in 2003 at the age of 18 and has earned more than 200 caps, making him history's most-capped male player.[8] Ronaldo has played in eleven major tournaments and scored in ten; he scored his first international goal at Euro 2004, where he helped Portugal reach the final and subsequently made the team of the tournament. In the 2006 FIFA World Cup, his first World Cup, he was a focal part to Portugal ultimately finishing in fourth place. He assumed captaincy of the national team in July 2008 ahead of Euro 2008; four years later, at Euro 2012, he was named to the team of the tournament. In 2015, Ronaldo was named the best Portuguese player of all time by the Portuguese Football Federation. The following year, he led Portugal to their first major tournament title at Euro 2016, being named in the team of the tournament for the third time and receiving the Silver Boot as the second-highest goalscorer of the tournament. This achievement saw him receive his fourth Ballon d'Or. In 2018, Ronaldo had his most prolific World Cup campaign and was voted in the Fan Dream Team. He led his country to victory in the inaugural UEFA Nations League in 2019, receiving the top scorer award in the finals, and also received the Golden Boot as top scorer of Euro 2020. In the 2022 World Cup, he became the first player to score at five World Cups.
One of the world's most marketable and famous athletes, Ronaldo was ranked the world's highest-paid athlete by Forbes in 2016, 2017, 2023, and 2024 and the world's most famous athlete by ESPN from 2016 to 2019. He is the first footballer and the third sportsman to earn US$1 billion in his career. Time included him on their list of the 100 most influential people in the world in 2014. Ronaldo is the most popular sportsperson on social media: he counts over 1 billion total followers across Facebook, Twitter, YouTube and Instagram, making him the first person to achieve that feat. Ronaldo was named in the UEFA Ultimate Team of the Year in 2015, the All-time UEFA Euro XI in 2016, and the Ballon d'Or Dream Team in 2020. In recognition of his record-breaking goalscoring success, he received special awards for Outstanding Career Achievement by FIFA in 2021 and Champions League All-Time Top Scorer by UEFA in 2024.
"""

if __name__ == "__main__":

    variable = "information"

    summary_prompt_template = PromptTemplate(
        input_variables=[variable],
        template=Templates.summary_template
    )

    llm = AzureChatOpenAI(
        azure_deployment=ModelDetails.AZURE_DEPLOYMENT_NAME,
        azure_endpoint=ModelDetails.AZURE_ENDPOINT,
        api_key=ModelDetails.AZURE_API_KEY,
        temperature=1,
        api_version=ModelDetails.AZURE_API_VERSION
    )

    chain = summary_prompt_template | llm
    response = chain.invoke({variable: information})
    print(response.content)
