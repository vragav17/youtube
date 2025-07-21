from src.prompt_engineering.prompt_templates import grouping_prompt_template

sample_comments = ["Invest in gold?", "Nippon GoldBees?", "Great job sir!"]
filled_prompt = grouping_prompt_template.format(comments="\n".join(sample_comments))
print(filled_prompt)
