import sys
sys.path.append('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator')
import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer


class BertQA:
    def __init__(self):
        # getting pre-trained model
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.questions = ["What event occurred?", "What was the exact date of the landslide?", "What was the exact location of the landslide?",
                          "How many people died in the landslide?", "How many people were injured in the landslide?", "How many people overall were affected by the landslide?",
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
    
    test_t ="""
        More than 120 people were killed in devastating floods and landslides caused by heavy rains in Rwanda, the government said on Wednesday, the highest death toll from a flood reported in a single day in the country’s recent history.

        Entire families were killed, injured or left homeless and in desperate need of assistance.

        “I wanted to cry but couldn’t in front of my children,” said Martine Nsanimana, 40, a resident of a small village in Western Rwanda whose home and farmland were destroyed by the floods.

        “If you saw how the farmland was washed away, you would want to cry,” said Mr. Nsanimana, a father of three.

        The rains started on Tuesday, but residents said that some people were still trapped in their homes on Wednesday, suggesting that the number of deaths could rise. Local officials also warned that more homes could fall down.

        Most of the casualties were recorded in the west and north of Rwanda, but some damage was also reported in the south. The districts of Ngororero, Rubavu, Nyabihu, Rutsiro, and Karongi, in the northwest, were among the hardest hit, the Rwandan government said.

        Videos showed swollen rivers of mud streaming through villages and alongside houses, and landslides of mud and rocks racing down hillsides into roads, homes and infrastructure.

        “Many houses collapsed on people,” said Francois Habitegeko, the governor of the Rwanda’s Western Province.

        Emergency workers were deployed to rescue those caught by the floods, helping the injured and those trapped in their homes.

        April is typically Rwanda’s rainiest month, but even for April the rains last month were heavy. And while the rainy season usually begins to wind down in May, the forecast called for more rain in the coming days.

        Experts said that the sandy soil and the terrain in the areas that were hit made them susceptible to floods and landslides.

        Joseph Tuyishimire, a researcher in geography at the University of Rwanda, said that the Western and Northern Provinces used to be natural forests, but had been converted into agricultural and settlement areas, increasing the risk of flooding.

        “If nothing is done to resolve this issue or relocate people from these areas,” said Mr. Tuyishimire, “we should expect consistent lethal floods.”

        Across East Africa in recent years, many areas, including in Uganda, Kenya and Somalia, have been experiencing both severe droughts and heavy rainfalls that kill many and damage properties and crops. In 2020, floods killed hundreds of people in the region.

        On Wednesday, the Red Cross in Uganda said that landslides had killed six people there, as well.

        Last year, a study found that human-caused climate change made heavy rains that lead to deadly floods in West Africa 80 times more likely. The scientists, part of the World Weather Attribution group, also found that the heavy rains that caused catastrophic flooding in South Africa last year had been made twice as likely by climate change.

        Mouhamadou Bamba Sylla, a Rwandan climate change scientist at the African Institute for Mathematical Sciences and an author with the United Nations Intergovernmental Panel on Climate Change, said that he could not say with certainty that Tuesday’s rainfalls were associated with climate change. But in general, he noted, climate change has increased the frequency and intensity of extreme rainfalls.

        The Rwandan government has promised to provide assistance to those in need, and relief efforts have already included helping bury victims and providing supplies to those whose homes were destroyed, Marie Solange Kayisire, a minister for emergencies, told reporters.

        “My deepest condolences to the families and loved ones of the victims of the landslides and floods that occurred last night,” Rwanda’s president, Paul Kagame, said on Twitter. “We are doing everything within our means to address this difficult situation.”

        Mr. Nsanimana’s house initially withstood the heavy rains on Tuesday, but eventually the flooding caused severe damage to its foundation, and it began to collapse.

        Mr. Nsanimana decided to move his family to his brother’s house in the north of the country, but he is not sure he will be able to afford to send them to school there.

        “I am now thinking of what to do next,” he said. “I don’t even know.”
    """
    print(obj.wrapper(test_t))