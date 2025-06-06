
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
'''
Model Details:
        Name: GPT-4o
        d_model: 8448.423119303523
        d_ff: 22529.128318142728
        Depth: 77
        Total FF Params: 351740204583.31104
        Total Embedding Params: 540699079.6354254
        Num Attention Heads: 57.0
        d_head: 150.09706298972918
        Group size: 7.125
        Total Attention Params: 12693515805.99087
        Total Params: 364974419468.9373
        Total Active Params: 101169266030.62637

FLOPS = 2 * ACTIVE_PARAMS * BATCH_SIZE * SEQ_LEN +
				4 * D_HEAD * NUM_QUERY_HEADS * LAYERS * MEAN_INPUT_LEN * BATCH_SIZE * SEQ_LEN

'''
import numpy as np
class Model:
    def __init__(self, name="None", d_model=3*2**12, d_ff=9*2**12, ff_matrix_count=(1, 1), layers=120, n_experts=1, n_active_experts=1, num_query_heads=128, group_size=1, \
                 weight_precision_bytes=2, activation_precision_bytes=2, d_head=None, vocab_size=0, parallel_attention=False):
        assert num_query_heads % group_size == 0

        # Variables directly set
        self.d_model = d_model
        self.d_ff = d_ff
        self.layers = layers
        self.n_experts = n_experts
        self.n_active_experts = n_active_experts
        self.num_query_heads = num_query_heads
        self.group_size = group_size
        self.weight_precision_bytes = weight_precision_bytes
        self.activation_precision_bytes = activation_precision_bytes
        self.vocab_size = vocab_size
        self.ff_matrix_count = ff_matrix_count
        self.parallel_attention = parallel_attention

        # Derived variables
        self.ff_params_per_layer_per_expert = sum(self.ff_matrix_count) * self.d_model * self.d_ff
        self.sparsity_factor = self.n_experts // self.n_active_experts
        self.total_ff_params = self.layers * self.n_experts * self.ff_params_per_layer_per_expert
        self.num_kv_heads = 2 * self.num_query_heads / self.group_size
        self.d_head = d_head if d_head != None else self.d_model // self.num_query_heads
        self.d_all_attn_heads = (self.num_query_heads + self.num_kv_heads) * self.d_head
        self.attn_params_per_layer = self.d_all_attn_heads * self.d_model + self.d_head*self.num_query_heads*self.d_model

        self.embedding_params = self.vocab_size * self.d_model * 2
        self.total_attn_params = self.layers * self.attn_params_per_layer
        self.total_params = self.total_attn_params + self.total_ff_params + self.embedding_params
        self.total_active_params = self.total_attn_params + self.total_ff_params//self.sparsity_factor + self.embedding_params

        self.kv_cache_size_per_input_bytes = self.num_kv_heads*self.d_head*self.layers*self.activation_precision_bytes

        self.name = name

    def __repr__(self):
        representation = f"""Model Details:
        Name: {self.name}
        d_model: {self.d_model}
        d_ff: {self.d_ff}
        Depth: {self.layers}
        Total FF Params: {self.total_ff_params}
        Total Embedding Params: {self.embedding_params}
        Num Attention Heads: {self.num_query_heads}
        d_head: {self.d_head}
        Group size: {self.group_size}
        Total Attention Params: {self.total_attn_params}
        Total Params: {self.total_params}
        Total Active Params: {self.total_active_params}
        """
        return representation

    def arithmetic_cost_flop(self, input_len, batch_size, seq_len=1, count_masked_flop=False):
        if count_masked_flop:
          mean_input_len = input_len + seq_len
        else:
          mean_input_len = (input_len + (input_len + seq_len - 1))/2

        # find cost to process prefill or decoding
        # this scales quadratically with seq_len because mean_input_len is proportion to seq_len
        return (2*self.total_active_params*batch_size*seq_len + 4*self.d_head*self.num_query_heads*self.layers*mean_input_len*batch_size*seq_len)

# Mixtral 8x22B is an open-weight model with known architecture
Mixtral_8x22B = Model(name="Mixtral 8x22B",
                      d_model=6144,
                      d_ff=16384,
                      ff_matrix_count=(2, 1),
                      layers=56,
                      n_experts=8,
                      n_active_experts=2,
                      num_query_heads=48,
                      d_head=128,
                      group_size=6,
                      activation_precision_bytes=2,
                      weight_precision_bytes=2,
                      vocab_size=32000
)

def scale_model(name, model: Model, scale_factor: float, depth_exponent=1/3):
    d_model = model.d_model * scale_factor**((1 - depth_exponent)/2)
    d_ff = model.d_ff * scale_factor**((1 - depth_exponent)/2)
    layers = int(model.layers * scale_factor**(depth_exponent))

    num_query_heads = np.ceil(model.num_query_heads * scale_factor**((1 - depth_exponent)/4))
    num_groups = model.num_query_heads/model.group_size
    group_size = num_query_heads/num_groups

    return Model(name=name,
                 d_model=d_model,
                 d_ff=d_ff,
                 ff_matrix_count=model.ff_matrix_count,
                 layers=layers,
                 n_experts=model.n_experts,
                 n_active_experts=model.n_active_experts,
                 num_query_heads=num_query_heads,
                 group_size=group_size,
                 d_head=model.d_head * scale_factor**((1 - depth_exponent)/4),
                 weight_precision_bytes=model.weight_precision_bytes,
                 activation_precision_bytes=model.activation_precision_bytes,
                 vocab_size=model.vocab_size,
                 parallel_attention=model.parallel_attention
                 )

# This produces an estimate of GPT-4o's parameters by scaling up Mixtral 8x22B so that it has 100B active parameters
GPT_4o = scale_model("GPT-4o", Mixtral_8x22B, 2.6)

def calculate_cost(input_len, output_len):
    model_obj = GPT_4o
    prefill_cost_flop = model_obj.arithmetic_cost_flop(input_len=0, batch_size=1, seq_len=input_len, count_masked_flop=True)
    decoding_cost_flop = model_obj.arithmetic_cost_flop(input_len=input_len, batch_size=1, seq_len=output_len)

    # assume 50% compute utilization during prefill. Kamath et. al. observed 70%: https://arxiv.org/pdf/2410.18038v1
    prefill_utilization = 0.5
    decoding_utilization = 0.1

    # H100 server consuming up to 1500 W per GPU.
    # Patel found ~100% TDP during prefill: https://www.microsoft.com/en-us/research/uploads/prod/2024/03/GPU_Power_ASPLOS_24.pdf
    gpu_power_draw_watts = 1500
    gpu_flop_per_second = 1e15

    gpu_joules_per_flop = gpu_power_draw_watts/gpu_flop_per_second
    prefill_cost_joules = (1/prefill_utilization) * prefill_cost_flop*gpu_joules_per_flop/3600
    decoding_cost_joules = (1/decoding_utilization) * decoding_cost_flop*gpu_joules_per_flop/3600
 
    print("FLOP and Wh cost for input length %d and output length %d:" % (input_len, output_len))

    print("Prefill cost: %.2e FLOP, %.3f Wh" % (prefill_cost_flop, prefill_cost_joules))
    print("Decoding cost: %.2e FLOP, %.3f Wh" % (decoding_cost_flop, decoding_cost_joules))
    
    return prefill_cost_joules + decoding_cost_joules

