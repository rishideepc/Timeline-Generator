import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer


class BertQA:
    def __init__(self):
        # getting pre-trained model
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.questions = ["What event occurred?", "When did the landslide occur?", "Where did the landslide happen?",
                          "How many people died?", "How many people were injured?", "How many people were affected?",
                          "How severe was the landslide?"]
        self.answers = {i:"" for i in range(1,8)}
        self.text = ""

    # function for QA
    def question_answer(self, question):
        # tokenize question and text as a pair
        input_ids = self.tokenizer.encode(question, self.text)

        # string version of tokenized ids
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids)

        # segment IDs
        # first occurence of [SEP] token
        sep_idx = input_ids.index(self.tokenizer.sep_token_id)
        # number of tokens in segment A (question)
        num_seg_a = sep_idx + 1
        # number of tokens in segment B (text)
        num_seg_b = len(input_ids) - num_seg_a

        # list of 0s and 1s for segment embeddings
        segment_ids = [0] * num_seg_a + [1] * num_seg_b
        assert len(segment_ids) == len(input_ids)

        # model output using input_ids and segment_ids
        output = self.model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))

        # reconstructing the answer
        answer_start = torch.argmax(output.start_logits)
        answer_end = torch.argmax(output.end_logits)
        answer = "[CLS]"
        if answer_end >= answer_start:
            answer = tokens[answer_start]
            for i in range(answer_start + 1, answer_end + 1):
                if tokens[i][0:2] == "##":
                    answer += tokens[i][2:]
                else:
                    answer += " " + tokens[i]

        if answer.startswith("[CLS]"):
            answer = "Negative"

        return answer.capitalize()

    def wrapper(self, text):
        self.text = text
        for i, question in enumerate(self.questions):
            self.answers[i+1] = self.question_answer(question)
        return self.answers


if __name__ == '__main__':
    obj = BertQA()
    t = "Heavy rains in coastal areas of Brazil's southeast have caused flooding and landslides and killed more than " \
        "35 in the city of Sao Sebastiao. Hundreds of residents were dislodged, according to media reports. Rescue " \
        "workers continue to look for victims, reconnect isolated communities and clear roads. Heavy rainfall in " \
        "Brazil has led to flooding and landslides. More than 35 people have died due to the landslides. The rescue " \
        "workers continued to look for victims, reconnect isolated communities and clear roads where several " \
        "residents were trapped. A car covered with mud was seen as a woman looks from inside her house in one of the " \
        "landslide sites after severe rainfall at Barra do Sahy in Sao Sebastiao. Volunteers and firefighters worked " \
        "to find victims in one of the landslides sites after severe rainfall at Barra do Sahy in Sao Sebastiao. Sao " \
        "Paulo’s state government said in a statement that 35 died in the city of Sao Sebastiao and a 7-year-old girl " \
        "was killed in neighboring Ubatuba. A dog covered in mud was seen at one of the landslide sites after severe " \
        "rainfall at Barra do Sahy. A small TV covered in mud was seen in one of the landslides sites. Many buildings " \
        "were damaged due to landslides and flooding. Several deadly landslides were seen after severe rainfall at " \
        "Barra do Sahy, in Sao Sebastiao, Brazil on Tuesday. "
    print(obj.wrapper(t))