import torch
print("Torch version:",torch.__version__)

print("Is CUDA enabled?",torch.cuda.is_available())
print(torch.backends.cuda.flash_sdp_enabled())
# True
print(torch.backends.cuda.mem_efficient_sdp_enabled())
# True
print(torch.backends.cuda.math_sdp_enabled())
# True

with torch.backends.cuda.sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=False):
    print(torch.backends.cuda.flash_sdp_enabled())
    # True
    print(torch.backends.cuda.mem_efficient_sdp_enabled())
    # False
    print(torch.backends.cuda.math_sdp_enabled())
    # False