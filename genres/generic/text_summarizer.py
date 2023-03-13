############## USING SUMY LexRank ##############################
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer


text = '''
A vaccine for the coronavirus will likely be ready by early 2021 but rolling it out safely across India’s 1.3 billion people will be the country’s biggest challenge in fighting its surging epidemic, a leading vaccine scientist told Bloomberg.
India, which is host to some of the front-runner vaccine clinical trials, currently has no local infrastructure in place to go beyond immunizing babies and pregnant women, said Gagandeep Kang, professor of microbiology at the Vellore-based Christian Medical College and a member of the WHO’s Global Advisory Committee on Vaccine Safety.
The timing of the vaccine is a contentious subject around the world. In the U.S., President Donald Trump has contradicted a top administration health expert by saying a vaccine would be available by October. In India, Prime Minister Narendra Modi’s government had promised an indigenous vaccine as early as mid-August, a claim the government and its apex medical research body has since walked back.
'''
parser= PlaintextParser.from_string(text, Tokenizer("english"))

from sumy.summarizers.text_rank import TextRankSummarizer 
summarizer = TextRankSummarizer()
summary= summarizer(parser.document, 1)
text_summary=""

for sentence in summary:
    text_summary+=str(sentence)

print("TEXT SUMMARY: ", text_summary)


############## USING Gensim ###################################
# from gensim.summarization.summarizer import summarize
# from gensim.summarization import keywords
# import wikipedia
# import en_core_web_sm

# wikisearch = wikipedia.page("")
# wikicontent = wikisearch.content
# nlp = en_core_web_sm.load()
# doc = nlp(wikicontent)

# summ_words = summarize(wikicontent, word_count = "")
# print("Word count summary")
# print(summ_words)

