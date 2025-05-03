import runpod
import torch

def get_gpu_info():
    """
    Get information about available GPUs including count and memory.
    """
    gpu_info = {
        "gpu_available": torch.cuda.is_available(),
        "gpu_count": 0,
        "gpu_memory": []
    }
    
    if gpu_info["gpu_available"]:
        gpu_info["gpu_count"] = torch.cuda.device_count()
        
        # Get memory info for each GPU
        for i in range(gpu_info["gpu_count"]):
            gpu_memory = {
                "device_name": torch.cuda.get_device_name(i),
                "total_memory_GB": round(torch.cuda.get_device_properties(i).total_memory / (1024**3), 2)
            }
            gpu_info["gpu_memory"].append(gpu_memory)
    
    return gpu_info

def handler(job):
    """
    This is a handler that returns GPU information and a greeting.
    The job parameter contains the input data in job["input"]
    """
    job_input = job["input"]
    
    # Get the name from the input, default to "World" if not provided
    name = job_input.get("name", "World")
    
    # Get GPU information
    gpu_info = get_gpu_info()
    
    # Prepare response
    response = {
        "greeting": f"Hello, {name}! Welcome to RunPod Serverless!",
        "gpu_info": gpu_info
    }
    
    return response

# Start the serverless function
runpod.serverless.start({"handler": handler})
