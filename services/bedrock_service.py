import boto3

class BedrockService:
    def __init__(self, model_name, prompt_template):
        self.model_name = model_name
        self.prompt_template = prompt_template
        self.client = boto3.client('bedrock')

    def create_prompt(self, input_data):
        return self.prompt_template.format(input_data=input_data)

    def invoke_model(self, input_data):
        prompt = self.create_prompt(input_data)
        response = self.client.invoke_model(
            ModelName=self.model_name,
            Body=prompt
        )
        return response['Body'].read().decode('utf-8')

    def stream_responses(self, input_data):
        prompt = self.create_prompt(input_data)
        # Here implement streaming logic using the relevant SDK feature
        # This is a placeholder for the actual streaming implementation.

    def inject_context(self, kendra_results):
        # Context injection logic based on Kendra search results
        # Process the Kendra results to enhance the prompt
        context = "".join(kendra_results)
        return context

if __name__ == '__main__':
    # Example usage
    kendra_results = ['result1', 'result2']  # Replace with actual Kendra results
    context = BedrockService.inject_context(kendra_results)
    service = BedrockService(model_name='Claude', prompt_template='Input: {input_data} \n Context: {context}')
    response = service.invoke_model(input_data='Example input')
    print(response)