
import gradio as gr
from shared.utils.plugins import WAN2GPPlugin
import json
import os

class Wan2GPLocalizationPlugin(WAN2GPPlugin):
    def __init__(self):
        super().__init__()
        self.name = "Chinese-Simplified"
        self.version = "1.0.0"
        self.description = "Translates Wan2GP UI to Chinese."
        self.translations = {}
        self.ui_root = None

    def load_translations(self):
        try:
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(plugin_dir, "translations.json")
            with open(json_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
            print(f"[Localization] Loaded {len(self.translations)} translations.")
        except Exception as e:
            print(f"[Localization] Error loading translations: {e}")

    def setup_ui(self):
        self.load_translations()
        # Request access to a known component to find the root
        self.request_component("video_gen")

    def post_ui_setup(self, components: dict):
        video_gen_tab = components.get("video_gen")
        if not video_gen_tab and hasattr(self, "video_gen"):
             video_gen_tab = self.video_gen

        if not video_gen_tab:
            print("[Localization] 'video_gen' component not found in insertion dict or self.video_gen. Cannot traverse UI yet.")
            return

        # Traverse up to find the root Blocks
        root = video_gen_tab
        while hasattr(root, "parent") and root.parent is not None:
            root = root.parent
            
        print("[Localization] Found UI root, starting translation...")
        self.translate_recursive(root)
        print("[Localization] Translation complete.")

    def translate_text(self, text):
        if not isinstance(text, str):
            return text
        translation = self.translations.get(text)
        if translation:
            return translation
        else:
            # Check for debug flag (Env var 'WAN2GP_I18N_DEBUG' or internal flag)
            # Default is True to help find missing strings, set to '0' or 'False' to disable.
            debug_env = os.environ.get("WAN2GP_I18N_DEBUG", "True").lower()
            if debug_env in ["true", "1", "yes"] and text and len(text.strip()) > 0 and not text.isdigit():
                 print(f"[Localization] Missing translation for: '{text}'")
            return text

    def translate_recursive(self, component):
        # Translate attributes if present
        if hasattr(component, "label") and component.label:
            component.label = self.translate_text(component.label)
        
        if hasattr(component, "info") and component.info:
            component.info = self.translate_text(component.info)
            
        # For buttons, value is the label
        if isinstance(component, gr.Button) and hasattr(component, "value"):
             component.value = self.translate_text(component.value)
             
        # For Markdown/HTML, value is the content
        if isinstance(component, (gr.Markdown, gr.HTML)) and hasattr(component, "value"):
             component.value = self.translate_text(component.value)

        # For Dropdown/Radio/CheckboxGroup, translate choices (keep value)
        if isinstance(component, (gr.Dropdown, gr.Radio, gr.CheckboxGroup)) and hasattr(component, "choices"):
             if component.choices:
                 new_choices = []
                 for choice in component.choices:
                     if isinstance(choice, str):
                         # Convert "Value" -> ("Translated", "Value")
                         translated = self.translate_text(choice)
                         new_choices.append((translated, choice))
                     elif isinstance(choice, (list, tuple)) and len(choice) == 2:
                         # Update label in existing tuple ("Label", "Value") -> ("Translated", "Value")
                         label, val = choice
                         translated_label = self.translate_text(label)
                         new_choices.append((translated_label, val))
                     else:
                         new_choices.append(choice)
                 component.choices = new_choices
        
        # Recursive step
        if hasattr(component, "children") and isinstance(component.children, list):
            for child in component.children:
                self.translate_recursive(child)
