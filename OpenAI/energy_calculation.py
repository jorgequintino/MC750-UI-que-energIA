
#	RESUMO DO SITE https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use:

# ESSE NOTEBOOK FOI O QUE ELES UTILIZARAM PARA OS CÁLCULOS DELES, VOU DEIXAR AQUI PARA VCS PODEREM VER

'''
typical ChatGPT queries using GPT-4o likely consume roughly 0.3 watt-hours
 
0.3 watt-hours is less than the amount of electricity that an LED lightbulb or a laptop consumes in a few minutes

How to estimate the compute and energy cost of a ChatGPT query?

	Choose a model:
 
	Token: 0.75 words on avg
		Each token requires 2 FLOP for every active parameter in the model

	GPT-4o : ~200 billion parameters
			Pessimistically: ~100 billion active parameters activated per query
   
   -> 200 bilion FLOP p/ token
   
   
   ESTIMATIVE OF FLOP: OUTPUT_TOKENS * 2 * NUM_ACTIVE_PARAMETERS
	
 
	ENERGY CONSUMPTION:
	
	OpenAI uses Nvidia H100 GPUs for ChatGPT.
	~1500W per GPU (700W from GPU and 800W from servers and data centers)
	
	Each H100 performs 989 trillion FLOP p/s, 
 	Typically only 10% power is used.

 
	ENERGY FORMULA: (NUM_FLOPS) / (GPU_PROCESSING_SPEED) * 10 * 0.7 * (GPU_POWER)

	
	CONSIDERANDO O TAMANHO DO INPUT	
		FLOPS = 2 * ACTIVE_PARAMS * BATCH_SIZE * SEQ_LEN +
				4 * D_HEAD * NUM_QUERY_HEADS * LAYERS * MEAN_INPUT_LEN * BATCH_SIZE * SEQ_LEN
	
 	O segundo termo vêm do tratamento do input (Attention Mechanism)
'''
	
'''
IDEIAS:
	- Procurar dados de vários modelos
		- GPT
		- GEMINI
		- DEEPSEEK
	- Tentar variar as GPUS, ai poderíamos verificar o quanto de energia seria gasta se uma placa de vídeo normal fosse utilizada
			- Faria sentido para um usuário mais "entendedor" mas não pro público geral
	

'''