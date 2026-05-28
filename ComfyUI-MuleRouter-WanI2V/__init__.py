from .nodes import MuleRouterWanI2VNode

NODE_CLASS_MAPPINGS = {
    "MuleRouterWanI2VNode": MuleRouterWanI2VNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MuleRouterWanI2VNode": "MuleRouter I2V (Wan2.7)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']