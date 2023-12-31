import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList, GenerationConfig
import torch
import os, argparse


class StoppingCriteriaSub(StoppingCriteria):

    def __init__(self, stops = [], encounters=1):
      super().__init__()
      self.stops = stops
      self.encounters = encounters
      self.counter = 0

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        for stop in self.stops:
                if torch.all((stop == input_ids[0][-len(stop):])).item():
                    self.counter += 1
        if self.counter >= self.encounters:
            return True
        else:
            return False

####################################################################################
# python inference.py --model_path "KRAFTON/KORani-v1-13B" --task "translation"


if __name__ == "__main__" :

    parser = argparse.ArgumentParser()

    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--task", type=str, default="translation")    
    parser.add_argument("--model_max_length", type=int, default=2048)

    args = parser.parse_args()

    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3" # if you want to use more gpus, set more numbers
    # os.environ["CUDA_VISIBLE_DEVICES"] = "" # if you want to use more gpus, set more numbers

    print(args.model_path)
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        args.model_path,
        model_max_length=args.model_max_length,
        padding_side="right",
        use_fast=False,
        return_token_type_ids=False,
    )
    model = transformers.AutoModelForCausalLM.from_pretrained(args.model_path, device_map="auto", torch_dtype=torch.float16)        
    model.eval()


####################################################################################################

    # with open(f"prompts/{args.task}.txt") as f:
    #     prompt = "".join(f.readlines())
    
    
    
    
    
    # batch = tokenizer(prompt, return_tensors="pt")
    # prompt_size = len(batch['input_ids'][0])
    # batch = {k: v.cuda() for k, v in batch.items()}
    
    
    
    



    # #It is the definition of stop tokens by instruct tuning. You can omit or add to it as you prefer. e.g. '\n### Human:'
    # stop_tokens = [[13, 2277, 29937, 12968, 29901],[535],[187,187],[13,13], [13, 2277, 29937, 4007, 22137],[13, 2659, 29901],[202, 6], [6,6,6], [6805, 341, 29]]
    # stop_words_ids = [torch.tensor(stop_word).to(device='cuda', dtype=torch.int64) for stop_word in stop_tokens]
    # encounters = 1
    # stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids, encounters=encounters)])
    # generation_config = GenerationConfig(
    #     temperature = 0.1,
    #     max_new_tokens = 512,
    #     exponential_decay_length_penalty = (512, 1.03),
    #     eos_token_id = tokenizer.eos_token_id,
    #     repetition_penalty = 1.05,
    #     do_sample = False,
    #     top_p = 0.7,
    #     min_length = 5,
    #     use_cache = True,
    #     return_dict_in_generate = True,
    # )
    # if 'token_type_ids' in batch:
    #     del batch['token_type_ids']
    # generated = model.generate(**batch, generation_config=generation_config, stopping_criteria=stopping_criteria)
    # response = tokenizer.decode(generated['sequences'][0][prompt_size:], skip_special_tokens=True)
    
    # # post-processing
    # response = response.split("#")[0]
    
    
    
    # print(response)


##########################################################################################

    
    flag = 1
    while(flag ==1):
        dynamic_input = input("dynamic input:  ")
        if(dynamic_input == "exit"):
            flag = 2
            exit()
        prompt =dynamic_input+"\n### Assistant:"
        batch = tokenizer(prompt, return_tensors="pt")
        prompt_size = len(batch['input_ids'][0])
        batch = {k: v.cuda() for k, v in batch.items()}




        # It is the definition of stop tokens by instruct tuning. You can omit or add to it as you prefer. e.g. '\n### Human:'
        stop_tokens = [[13, 2277, 29937, 12968, 29901],[535],[187,187],[13,13], [13, 2277, 29937, 4007, 22137],[13, 2659, 29901],[202, 6], [6,6,6], [6805, 341, 29]]

        stop_words_ids = [torch.tensor(stop_word).to(device='cuda', dtype=torch.int64) for stop_word in stop_tokens]
        encounters = 1
        stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids, encounters=encounters)])

        generation_config = GenerationConfig(
            temperature = 0.1,
            max_new_tokens = 512,
            exponential_decay_length_penalty = (512, 1.03),
            eos_token_id = tokenizer.eos_token_id,
            repetition_penalty = 1.05,
            do_sample = False,
            top_p = 0.7,
            min_length = 5,
            use_cache = True,
            return_dict_in_generate = True,
        )
        if 'token_type_ids' in batch:
            del batch['token_type_ids']
        generated = model.generate(**batch, generation_config=generation_config, stopping_criteria=stopping_criteria)
        response = tokenizer.decode(generated['sequences'][0][prompt_size:], skip_special_tokens=True)
        
        # post-processing
        response = response.split("#")[0]
        
        print(response)
        
        
##########################################################################################