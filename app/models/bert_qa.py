import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer


class BertQA:
    def __init__(self):
        # getting pre-trained model
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.questions = ["What event occurred?", "What was the exact date of the landslide?",
                          "What was the exact location of the landslide?",
                          "How many people died in the landslide?", "How many people were injured in the landslide?",
                          "How many people overall were affected by the landslide?",
                          "How severe was the landslide?"]
        self.answers = {i: "" for i in range(1, 8)}
        self.text = ""

    # function for QA
    def question_answer(self, question):
        # tokenize question and text as a pair
        input_ids = self.tokenizer.encode(question, self.text, max_length=100)

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
            self.answers[i + 1] = self.question_answer(question)
        return self.answers

