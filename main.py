"""
FolderCrafter - A Modern Folder Structure Generator
Built with CustomTkinter
Theme: Modern SaaS (Indigo/Gray)
"""

import customtkinter as ctk
import os
import json
import sys
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
import webbrowser


class CTkToolTip:
    """Simple tooltip for CustomTkinter widgets."""
    def __init__(self, widget, message):
        self.widget = widget
        self.message = message
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    
    def show(self, event=None):
        x, y = self.widget.winfo_rootx() + 25, self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip, 
            text=self.message, 
            background="#333333", 
            foreground="white",
            relief="flat", 
            padx=8, 
            pady=4,
            font=("Segoe UI", 10)
        )
        label.pack()
    
    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# ============================================================================
# MODERN COLOR PALETTE
# ============================================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Modern SaaS Colors
COLOR_PRIMARY = "#6366f1"      # Indigo
COLOR_PRIMARY_HOVER = "#818cf8"
COLOR_SUCCESS = "#22c55e"      # Green
COLOR_DANGER = "#ef4444"       # Red (for delete only)
COLOR_WARNING = "#f59e0b"      # Amber

COLOR_BG_DARK = "#0f0f0f"      # Deepest background
COLOR_BG = "#1a1a1a"           # Main background
COLOR_SURFACE = "#252525"      # Card background
COLOR_SURFACE_LIGHT = "#2f2f2f" # Lighter surface
COLOR_BORDER = "#3a3a3a"       # Subtle borders

COLOR_TEXT = "#ffffff"         # Primary text
COLOR_TEXT_MUTED = "#a1a1aa"   # Muted/subtitle text
COLOR_TEXT_DIM = "#71717a"     # Very dim text

SAVE_FILE = "foldercrafter_templates.json"

# ============================================================================
# DEFAULT TEMPLATES
# ============================================================================
DEFAULT_TEMPLATES = {
    "Film / Video": [
        "01 Project/01 Premiere",
        "01 Project/02 After Effects",
        "02 Assets/01 Footage",
        "02 Assets/02 Stock",
        "02 Assets/03 Audio/01 Location Sound",
        "02 Assets/03 Audio/02 ADR",
        "02 Assets/03 Audio/03 SFX",
        "02 Assets/03 Audio/04 Music",
        "02 Assets/04 Graphics/01 Logos",
        "02 Assets/04 Graphics/02 Credits",
        "02 Assets/04 Graphics/03 Photos",
        "02 Assets/04 Graphics/04 Graphic Elements",
        "03 Docs",
        "04 Exports",
        "05 Stuff",
    ],
    "AI Video Production": [
        "01 Project/01 Premiere",
        "01 Project/02 After Effects",
        "01 Project/03 Photoshop",
        "02 REFS/01 Locations",
        "02 REFS/02 Characters",
        "02 REFS/03 Moodboard",
        "03 Assets/01 Working Frames",
        "03 Assets/02 Frames",
        "03 Assets/03 Videos",
        "03 Assets/04 Audio/01 Recording",
        "03 Assets/04 Audio/02 SFX",
        "03 Assets/04 Audio/03 Ambience",
        "03 Assets/04 Audio/04 Music",
        "03 Assets/05 Graphics/01 Logos",
        "03 Assets/05 Graphics/02 Graphic Elements",
        "04 Exports",
        "05 Stuff",
    ],
    "Web Project": [
        "src",
        "src/assets/images",
        "src/assets/fonts",
        "src/components",
        "src/styles",
        "public",
    ],
    "Data Science": [
        "data/raw",
        "data/processed",
        "notebooks",
        "src/models",
        "src/visualization",
    ],
    "Photo Archive": [
        "Photos",
        "Edited",
        "Exports",
    ],
    "Game Dev": [
        "Assets/Sprites",
        "Assets/Audio",
        "Scripts",
        "Scenes",
    ],
}


def load_templates():
    """Load templates, merging defaults with any saved user templates."""
    save_path = Path.home() / ".foldercrafter" / SAVE_FILE
    
    # Start with default templates
    templates = DEFAULT_TEMPLATES.copy()
    
    # Merge with saved templates (user templates override defaults with same name)
    if save_path.exists():
        try:
            with open(save_path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                templates.update(saved)
        except Exception:
            pass
    
    return templates


def save_templates(templates):
    save_path = Path.home() / ".foldercrafter" / SAVE_FILE
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=2)


def parse_indented_lines(text):
    """Converts indented text to full paths."""
    paths = []
    stack = []
    
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        
        indent = len(line) - len(line.lstrip())
        name = line.strip()
        
        while stack and stack[-1][0] >= indent:
            stack.pop()
        
        stack.append((indent, name))
        full_path = "/".join([x[1] for x in stack])
        paths.append(full_path)
    
    return paths


def format_paths_to_tree(paths):
    """Converts full paths to tree-like text display."""
    if not paths:
        return "  No folders to preview"
    
    all_paths = set()
    for p in paths:
        parts = p.split('/')
        for i in range(1, len(parts) + 1):
            all_paths.add("/".join(parts[:i]))
    
    sorted_paths = sorted(list(all_paths))
    
    lines = []
    for p in sorted_paths:
        parts = p.split('/')
        depth = len(parts) - 1
        name = parts[-1]
        
        if depth == 0:
            prefix = "📁  "
        else:
            prefix = "    " * depth + "└── "
        lines.append(f"{prefix}{name}")
    
    return "\n".join(lines)


def format_paths_to_indented(paths):
    """Converts full paths to indented text for editing."""
    if not paths:
        return ""
    
    all_paths = set()
    for p in paths:
        parts = p.split('/')
        for i in range(1, len(parts) + 1):
            all_paths.add("/".join(parts[:i]))
    
    sorted_paths = sorted(list(all_paths))
    
    lines = []
    for p in sorted_paths:
        parts = p.split('/')
        depth = len(parts) - 1
        name = parts[-1]
        indent = "    " * depth
        lines.append(f"{indent}{name}")
    
    return "\n".join(lines)


# ============================================================================
# MAIN APPLICATION
# ============================================================================
class FolderCrafterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("FolderCrafter")
        self.geometry("1100x700")
        
        # Set Icon
        try:
            icon_path = resource_path("foldercrafter.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass  # Icon might not exist in dev env or different OS

        # Design System (Modern Palette - Slate & Indigo)
        # Backgrounds
        self.color_bg = "#0f172a"        # Very dark slate
        self.color_surface = "#1e293b"   # Slate 800
        self.color_surface_light = "#334155" # Slate 700
        
        # Accents
        self.color_primary = "#6366f1"   # Indigo 500
        self.color_primary_hover = "#4f46e5" # Indigo 600
        self.color_secondary = "#a855f7" # Purple 500 (Gradients)
        
        # Text
        self.color_text = "#f8fafc"      # Slate 50
        self.color_text_muted = "#94a3b8"# Slate 400
        
        # Status
        self.color_success = "#10b981"   # Emerald 500
        self.color_error = "#ef4444"     # Red 500
        self.color_warning = "#f59e0b"   # Amber 500

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # State
        self.templates = load_templates()
        self.selected_template = list(self.templates.keys())[0] if self.templates else None
        self.editing_template = None
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        self.create_main_content()
        
        # Check command line arguments (Context Menu Support)
        if len(sys.argv) > 1:
            initial_path = sys.argv[1]
            # Strip quotes if present (Windows sometimes adds them)
            initial_path = initial_path.strip('"')
            
            if os.path.isdir(initial_path) and hasattr(self, 'target_entry'):
                self.target_entry.delete(0, 'end')
                self.target_entry.insert(0, initial_path)

        
        # Show generator by default
        self.show_generator()
    
    def create_sidebar(self):
        """Create a minimal, elegant sidebar."""
        self.sidebar = ctk.CTkFrame(
            self, 
            width=220, 
            corner_radius=0, 
            fg_color=COLOR_BG,
            border_width=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)
        self.sidebar.grid_propagate(False)
        
        # App Logo/Brand
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.grid(row=0, column=0, padx=24, pady=(32, 40), sticky="w")
        
        logo_label = ctk.CTkLabel(
            brand_frame,
            text="📂",
            font=ctk.CTkFont(size=28)
        )
        logo_label.grid(row=0, column=0, padx=(0, 12))
        
        title_label = ctk.CTkLabel(
            brand_frame,
            text="FolderCrafter",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXT
        )
        title_label.grid(row=0, column=1)
        
        # Navigation Section
        nav_label = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLOR_TEXT_DIM
        )
        nav_label.grid(row=1, column=0, padx=24, pady=(0, 12), sticky="w")
        
        # Navigation buttons with modern styling
        self.btn_generator = ctk.CTkButton(
            self.sidebar,
            text="  🚀  Craft",
            font=ctk.CTkFont(size=14),
            height=44,
            anchor="w",
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=10,
            command=self.show_generator
        )
        self.btn_generator.grid(row=2, column=0, padx=16, pady=4, sticky="ew")
        
        self.btn_templates = ctk.CTkButton(
            self.sidebar,
            text="  📝  Templates",
            font=ctk.CTkFont(size=14),
            height=44,
            anchor="w",
            fg_color="transparent",
            hover_color=COLOR_SURFACE_LIGHT,
            corner_radius=10,
            text_color=COLOR_TEXT_MUTED,
            command=self.show_templates
        )
        self.btn_templates.grid(row=3, column=0, padx=16, pady=4, sticky="ew")
        
        self.btn_howto = ctk.CTkButton(
            self.sidebar,
            text="  ❓  How to Use",
            font=ctk.CTkFont(size=14),
            height=44,
            anchor="w",
            fg_color="transparent",
            hover_color=COLOR_SURFACE_LIGHT,
            corner_radius=10,
            text_color=COLOR_TEXT_MUTED,
            command=self.show_howto
        )
        self.btn_howto.grid(row=4, column=0, padx=16, pady=4, sticky="ew")
        
        # ========== FOOTER SECTION ==========
        # Buy Me a Coffee button
        bmc_btn = ctk.CTkButton(
            self.sidebar,
            text="☕ Buy me a Coffee",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            fg_color="#FFDD00",
            hover_color="#E5C700",
            text_color="#000000",
            corner_radius=10,
            command=lambda: webbrowser.open("https://www.buymeacoffee.com/craftedanomaly")
        )
        bmc_btn.grid(row=6, column=0, padx=16, pady=(20, 8), sticky="ew")
        
        # Crafted Anomaly branding
        brand_btn = ctk.CTkButton(
            self.sidebar,
            text="a crafted anomaly",
            font=ctk.CTkFont(size=11),
            height=24,
            fg_color="transparent",
            hover_color=COLOR_SURFACE_LIGHT,
            text_color=COLOR_TEXT_DIM,
            command=lambda: webbrowser.open("https://www.craftedanomaly.com")
        )
        brand_btn.grid(row=7, column=0, padx=24, pady=(0, 20))
    
    def create_main_content(self):
        """Create the main content area."""
        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        self.create_generator_view()
        self.create_templates_view()
        self.create_howto_view()
    
    def create_generator_view(self):
        """Create a beautiful centered card for the Generator."""
        self.generator_frame = ctk.CTkFrame(self.main_container, fg_color=COLOR_BG_DARK)
        self.generator_frame.grid_columnconfigure(0, weight=1)
        self.generator_frame.grid_rowconfigure(0, weight=1)  # Card area expands
        self.generator_frame.grid_rowconfigure(1, weight=0)  # Button stays fixed
        
        # Scrollable container for the card
        scroll_container = ctk.CTkScrollableFrame(
            self.generator_frame,
            fg_color=COLOR_BG_DARK,
            scrollbar_button_color=COLOR_SURFACE_LIGHT,
            scrollbar_button_hover_color=COLOR_BORDER
        )
        scroll_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        # Central Card (inside scrollable area)
        card = ctk.CTkFrame(
            scroll_container,
            fg_color=COLOR_SURFACE,
            corner_radius=20,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=0, column=0, padx=60, pady=(40, 20), sticky="ew")
        card.grid_columnconfigure(0, weight=1)
        
        # Card Header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=48, pady=(40, 32), sticky="w")
        
        title = ctk.CTkLabel(
            header_frame,
            text="⚡ Generate Folders",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLOR_TEXT
        )
        title.grid(row=0, column=0, sticky="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Create folder structures in seconds",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXT_MUTED
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))
        
        # Step 1: Template Selection
        step1_label = ctk.CTkLabel(
            card,
            text="① Select Template",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        step1_label.grid(row=1, column=0, padx=48, pady=(0, 8), sticky="w")
        
        template_names = list(self.templates.keys())
        self.template_var = ctk.StringVar(value=self.selected_template or "")
        
        self.template_menu = ctk.CTkOptionMenu(
            card,
            values=template_names,
            variable=self.template_var,
            command=self.on_template_change,
            width=500,
            height=48,
            font=ctk.CTkFont(size=14),
            fg_color=COLOR_SURFACE_LIGHT,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            dropdown_fg_color=COLOR_SURFACE,
            dropdown_hover_color=COLOR_SURFACE_LIGHT,
            corner_radius=10
        )
        self.template_menu.grid(row=2, column=0, padx=48, pady=(0, 24), sticky="ew")
        
        # Step 2: Preview
        step2_label = ctk.CTkLabel(
            card,
            text="② Preview Structure",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        step2_label.grid(row=3, column=0, padx=48, pady=(8, 8), sticky="w")
        
        preview_container = ctk.CTkFrame(
            card,
            fg_color=COLOR_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        preview_container.grid(row=4, column=0, padx=48, pady=(0, 24), sticky="ew")
        
        self.preview_textbox = ctk.CTkTextbox(
            preview_container,
            width=500,
            height=160,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            text_color=COLOR_TEXT_MUTED,
            state="disabled",
            wrap="none"
        )
        self.preview_textbox.pack(padx=16, pady=16, fill="both", expand=True)
        
        self.update_preview()
        
        # Step 3: Target Folder
        step3_label = ctk.CTkLabel(
            card,
            text="③ Choose Destination",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        step3_label.grid(row=5, column=0, padx=48, pady=(8, 8), sticky="w")
        
        target_frame = ctk.CTkFrame(card, fg_color="transparent")
        target_frame.grid(row=6, column=0, padx=48, pady=(0, 40), sticky="ew")
        target_frame.grid_columnconfigure(0, weight=1)
        
        self.target_entry = ctk.CTkEntry(
            target_frame,
            height=48,
            font=ctk.CTkFont(size=14),
            fg_color=COLOR_SURFACE_LIGHT,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=10,
            placeholder_text="Click Browse to select a folder..."
        )
        self.target_entry.grid(row=0, column=0, padx=(0, 12), sticky="ew")
        
        browse_btn = ctk.CTkButton(
            target_frame,
            text="📁 Browse",
            width=120,
            height=48,
            font=ctk.CTkFont(size=14),
            fg_color=COLOR_SURFACE_LIGHT,
            hover_color=COLOR_BORDER,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=10,
            command=self.browse_folder
        )
        browse_btn.grid(row=0, column=1)
        
        # ========== FIXED BOTTOM BUTTON ==========
        button_container = ctk.CTkFrame(self.generator_frame, fg_color=COLOR_BG_DARK)
        button_container.grid(row=1, column=0, sticky="ew", padx=60, pady=(0, 32))
        button_container.grid_columnconfigure(0, weight=1)
        
        create_btn = ctk.CTkButton(
            button_container,
            text="🚀  CRAFT",
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=14,
            command=self.create_folders
        )
        create_btn.grid(row=0, column=0, sticky="ew")
    
    def create_templates_view(self):
        """Create a modern split-screen template editor."""
        self.templates_frame = ctk.CTkFrame(self.main_container, fg_color=COLOR_BG_DARK)
        self.templates_frame.grid_columnconfigure(1, weight=1)
        self.templates_frame.grid_rowconfigure(0, weight=1)
        
        # ========== LEFT PANEL: Template List ==========
        list_panel = ctk.CTkFrame(
            self.templates_frame, 
            width=300, 
            fg_color=COLOR_BG,
            corner_radius=0
        )
        list_panel.grid(row=0, column=0, sticky="nsew")
        list_panel.grid_rowconfigure(2, weight=1)
        list_panel.grid_propagate(False)
        
        # Panel Header
        list_header = ctk.CTkLabel(
            list_panel,
            text="📚 Your Templates",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXT
        )
        list_header.grid(row=0, column=0, padx=24, pady=(28, 20), sticky="w")
        
        # New Template Button
        new_btn = ctk.CTkButton(
            list_panel,
            text="➕  New Template",
            font=ctk.CTkFont(size=14),
            height=44,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=10,
            command=self.new_template
        )
        new_btn.grid(row=1, column=0, padx=20, pady=(0, 16), sticky="ew")
        
        # Template List (Scrollable)
        self.template_list_frame = ctk.CTkScrollableFrame(
            list_panel, 
            fg_color="transparent",
            scrollbar_button_color=COLOR_SURFACE_LIGHT,
            scrollbar_button_hover_color=COLOR_BORDER
        )
        self.template_list_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 20))
        self.template_list_frame.grid_columnconfigure(0, weight=1)
        
        # Update grid weight for template list row
        list_panel.grid_rowconfigure(2, weight=1)
        
        self.refresh_template_list()
        
        # ========== RIGHT PANEL: Editor ==========
        editor_panel = ctk.CTkFrame(
            self.templates_frame,
            fg_color=COLOR_SURFACE,
            corner_radius=20,
            border_width=1,
            border_color=COLOR_BORDER
        )
        editor_panel.grid(row=0, column=1, sticky="nsew", padx=32, pady=32)
        editor_panel.grid_columnconfigure(0, weight=1)
        editor_panel.grid_columnconfigure(1, weight=1)
        editor_panel.grid_rowconfigure(4, weight=1)
        
        # Editor Header
        editor_title = ctk.CTkLabel(
            editor_panel,
            text="🛠️ Template Editor",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TEXT
        )
        editor_title.grid(row=0, column=0, columnspan=2, padx=32, pady=(28, 4), sticky="w")
        
        editor_subtitle = ctk.CTkLabel(
            editor_panel,
            text="Create and edit your folder structure templates",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT_DIM
        )
        editor_subtitle.grid(row=1, column=0, columnspan=2, padx=32, pady=(0, 24), sticky="w")
        
        # Template Name Input
        name_label = ctk.CTkLabel(
            editor_panel, 
            text="Template Name",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        name_label.grid(row=2, column=0, columnspan=2, padx=32, sticky="w", pady=(0, 6))
        
        self.editor_name_entry = ctk.CTkEntry(
            editor_panel,
            height=48,
            font=ctk.CTkFont(size=14),
            fg_color=COLOR_SURFACE_LIGHT,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=10,
            placeholder_text="e.g., My Project Template"
        )
        self.editor_name_entry.grid(row=3, column=0, columnspan=2, padx=32, sticky="ew", pady=(0, 20))
        
        # Two-Column Editor Area
        # Left: Structure Input
        structure_frame = ctk.CTkFrame(editor_panel, fg_color="transparent")
        structure_frame.grid(row=4, column=0, sticky="nsew", padx=(32, 8), pady=(0, 20))
        structure_frame.grid_rowconfigure(1, weight=1)
        structure_frame.grid_columnconfigure(0, weight=1)
        
        structure_label = ctk.CTkLabel(
            structure_frame, 
            text="📝 Folder Structure",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        structure_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        
        self.editor_structure_textbox = ctk.CTkTextbox(
            structure_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=COLOR_BG,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=10,
            wrap="none"
        )
        self.editor_structure_textbox.grid(row=1, column=0, sticky="nsew")
        self.editor_structure_textbox.bind("<KeyRelease>", self.update_editor_preview)
        
        # Hint below structure
        hint_label = ctk.CTkLabel(
            structure_frame,
            text="💡 Tip: Use 4 spaces to create subfolders",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_DIM
        )
        hint_label.grid(row=2, column=0, sticky="w", pady=(8, 0))
        
        # Right: Live Preview
        preview_frame = ctk.CTkFrame(editor_panel, fg_color="transparent")
        preview_frame.grid(row=4, column=1, sticky="nsew", padx=(8, 32), pady=(0, 20))
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        preview_label = ctk.CTkLabel(
            preview_frame, 
            text="👁️ Live Preview",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXT_MUTED
        )
        preview_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        
        self.editor_preview_textbox = ctk.CTkTextbox(
            preview_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=COLOR_BG,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=10,
            text_color=COLOR_TEXT_MUTED,
            state="disabled",
            wrap="none"
        )
        self.editor_preview_textbox.grid(row=1, column=0, sticky="nsew")
        
        # Status label for preview
        status_label = ctk.CTkLabel(
            preview_frame,
            text="Updates as you type",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_DIM
        )
        status_label.grid(row=2, column=0, sticky="w", pady=(8, 0))
        
        # Action Buttons Row
        btn_frame = ctk.CTkFrame(editor_panel, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=2, padx=32, pady=(0, 28), sticky="w")
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾  Save Template",
            width=160,
            height=48,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=COLOR_SUCCESS,
            hover_color="#16a34a",
            corner_radius=10,
            command=self.save_template
        )
        save_btn.grid(row=0, column=0, padx=(0, 8))
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=48,
            height=48,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color=COLOR_SURFACE_LIGHT,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=10,
            text_color=COLOR_TEXT_MUTED,
            command=self.new_template
        )
        CTkToolTip(clear_btn, message="Clear Editor")
        clear_btn.grid(row=0, column=1, padx=(0, 8))
        
        import_btn = ctk.CTkButton(
            btn_frame,
            text="⬇️",
            width=48,
            height=48,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color="#0d9488",
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=10,
            text_color=COLOR_TEXT_MUTED,
            command=self.import_template
        )
        CTkToolTip(import_btn, message="Import Template from JSON")
        import_btn.grid(row=0, column=2, padx=(0, 8))
        
        export_btn = ctk.CTkButton(
            btn_frame,
            text="⬆️",
            width=48,
            height=48,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",
            hover_color="#0d9488",
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=10,
            text_color=COLOR_TEXT_MUTED,
            command=self.export_template
        )
        CTkToolTip(export_btn, message="Export Template to JSON")
        export_btn.grid(row=0, column=3)
    
    def create_howto_view(self):
        """Create the How To guide view."""
        self.howto_frame = ctk.CTkFrame(self.main_container, fg_color=COLOR_BG_DARK)
        self.howto_frame.grid_columnconfigure(0, weight=1)
        self.howto_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable content
        scroll_container = ctk.CTkScrollableFrame(
            self.howto_frame,
            fg_color=COLOR_BG_DARK,
            scrollbar_button_color=COLOR_SURFACE_LIGHT,
            scrollbar_button_hover_color=COLOR_BORDER
        )
        scroll_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        # Content Card
        card = ctk.CTkFrame(
            scroll_container,
            fg_color=COLOR_SURFACE,
            corner_radius=20,
            border_width=1,
            border_color=COLOR_BORDER
        )
        card.grid(row=0, column=0, padx=60, pady=40, sticky="ew")
        card.grid_columnconfigure(0, weight=1)
        
        # Header
        title = ctk.CTkLabel(
            card,
            text="❓ How to Use FolderCrafter",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLOR_TEXT
        )
        title.grid(row=0, column=0, padx=48, pady=(40, 8), sticky="w")
        
        subtitle = ctk.CTkLabel(
            card,
            text="Your guide to creating folder structures effortlessly",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXT_MUTED
        )
        subtitle.grid(row=1, column=0, padx=48, pady=(0, 32), sticky="w")
        
        # Section 1: Generator
        self._add_howto_section(card, 2, 
            "⚡ Generator Tab",
            "The Generator is your main workspace for creating folders.",
            [
                "1️⃣  Select a template from the dropdown menu",
                "2️⃣  Preview the folder structure that will be created",
                "3️⃣  Click 'Browse' to choose your destination folder",
                "4️⃣  Hit the CRAFT button to create all folders instantly!"
            ]
        )
        
        # Section 2: Templates
        self._add_howto_section(card, 3,
            "📝 Templates Tab", 
            "Create and manage your custom folder templates.",
            [
                "• Click 'New Template' to start fresh",
                "• Give your template a memorable name",
                "• Type your folder structure using indentation:",
                "    src",
                "        components",
                "        styles",
                "    public",
                "• Use 4 spaces to create subfolders",
                "• The Live Preview shows your structure in real-time",
                "• Click 'Save Template' when you're done"
            ]
        )
        
        # Section 3: Tips
        self._add_howto_section(card, 4,
            "💡 Pro Tips",
            "Get the most out of FolderCrafter.",
            [
                "✨ Templates are saved automatically to your home folder",
                "✨ You can edit existing templates by clicking on them",
                "✨ Delete templates you no longer need with the ✕ button",
                "✨ Folder structures work on Windows, Mac, and Linux",
                "✨ Existing folders won't be overwritten - only new ones are created"
            ]
        )
        
        # Section 4: Examples
        self._add_howto_section(card, 5,
            "📁 Example Structures",
            "Here are some ideas to get you started.",
            [
                "Web Project:",
                "    src → components, styles, assets",
                "",
                "Python Project:",
                "    src → modules, utils, tests",
                "",
                "Photo Archive:",
                "    2024 → January, February, March...",
                "",
                "Game Development:",
                "    Assets → Sprites, Audio, Animations"
            ],
            is_last=True
        )
    
    def _add_howto_section(self, parent, row, title, description, items, is_last=False):
        """Helper to add a section to the how-to guide."""
        section = ctk.CTkFrame(parent, fg_color="transparent")
        section.grid(row=row, column=0, padx=48, pady=(0, 32 if not is_last else 48), sticky="ew")
        section.grid_columnconfigure(0, weight=1)
        
        # Section Title
        title_label = ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXT
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        
        # Section Description
        desc_label = ctk.CTkLabel(
            section,
            text=description,
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT_MUTED
        )
        desc_label.grid(row=1, column=0, sticky="w", pady=(0, 12))
        
        # Content box
        content_box = ctk.CTkFrame(
            section,
            fg_color=COLOR_BG,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER
        )
        content_box.grid(row=2, column=0, sticky="ew")
        
        # Items
        items_text = "\n".join(items)
        items_label = ctk.CTkLabel(
            content_box,
            text=items_text,
            font=ctk.CTkFont(family="Consolas", size=13),
            text_color=COLOR_TEXT_MUTED,
            justify="left",
            anchor="w"
        )
        items_label.grid(row=0, column=0, padx=20, pady=16, sticky="w")
    
    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    
    def show_generator(self):
        """Show the generator view."""
        self.templates_frame.grid_forget()
        self.howto_frame.grid_forget()
        self.generator_frame.grid(row=0, column=0, sticky="nsew")
        
        # Update nav button styles
        self.btn_generator.configure(fg_color=COLOR_PRIMARY, text_color=COLOR_TEXT)
        self.btn_templates.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)
        self.btn_howto.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)
        
        self.refresh_generator_menu()
    
    def show_templates(self):
        """Show the templates editor view."""
        self.generator_frame.grid_forget()
        self.howto_frame.grid_forget()
        self.templates_frame.grid(row=0, column=0, sticky="nsew")
        
        # Update nav button styles
        self.btn_generator.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)
        self.btn_templates.configure(fg_color=COLOR_PRIMARY, text_color=COLOR_TEXT)
        self.btn_howto.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)
    
    def show_howto(self):
        """Show the how-to guide view."""
        self.generator_frame.grid_forget()
        self.templates_frame.grid_forget()
        self.howto_frame.grid(row=0, column=0, sticky="nsew")
        
        # Update nav button styles
        self.btn_generator.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)
        self.btn_templates.configure(fg_color="transparent", text_color=COLOR_TEXT_MUTED)
        self.btn_howto.configure(fg_color=COLOR_PRIMARY, text_color=COLOR_TEXT)
    
    def on_template_change(self, value):
        """Handle template dropdown change."""
        self.selected_template = value
        self.update_preview()
    
    def update_preview(self):
        """Update the preview textbox in generator view."""
        template_name = self.selected_template
        if template_name and template_name in self.templates:
            tree_text = format_paths_to_tree(self.templates[template_name])
        else:
            tree_text = "  Select a template to preview..."
        
        self.preview_textbox.configure(state="normal")
        self.preview_textbox.delete("1.0", "end")
        self.preview_textbox.insert("1.0", tree_text)
        self.preview_textbox.configure(state="disabled")
    
    def browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(title="Select Target Folder")
        if folder:
            self.target_entry.delete(0, "end")
            self.target_entry.insert(0, folder)
    
    def create_folders(self):
        """Create the folder structure."""
        target = self.target_entry.get()
        template_name = self.selected_template
        
        if not target:
            messagebox.showwarning("Missing Folder", "Please select a destination folder first.")
            return
        
        if not template_name or template_name not in self.templates:
            messagebox.showwarning("No Template", "Please select a template from the dropdown.")
            return
        
        try:
            count = 0
            target_abs = os.path.abspath(target)
            
            for p in self.templates[template_name]:
                # Security: Prevent path traversal
                full_path = os.path.abspath(os.path.join(target_abs, p))
                
                # Check if the resolved path starts with the target path
                if not full_path.startswith(target_abs):
                    print(f"Skipping unsafe path: {p}", file=sys.stderr)
                    continue
                
                os.makedirs(full_path, exist_ok=True)
                count += 1
            
            messagebox.showinfo("Success! 🎉", f"Created {count} folders successfully!\n\nLocation: {target}")
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to create folders:\n{ex}")
    
    def refresh_template_list(self):
        """Refresh the template list in the sidebar."""
        for widget in self.template_list_frame.winfo_children():
            widget.destroy()
        
        for i, name in enumerate(self.templates.keys()):
            is_selected = (name == self.editing_template)
            
            item_frame = ctk.CTkFrame(
                self.template_list_frame,
                fg_color=COLOR_SURFACE if is_selected else "transparent",
                corner_radius=10
            )
            item_frame.grid(row=i, column=0, sticky="ew", pady=3)
            item_frame.grid_columnconfigure(0, weight=1)
            
            # Template button
            item_btn = ctk.CTkButton(
                item_frame,
                text=f"📁  {name}",
                anchor="w",
                height=40,
                fg_color="transparent",
                hover_color=COLOR_SURFACE_LIGHT,
                text_color=COLOR_TEXT if is_selected else COLOR_TEXT_MUTED,
                font=ctk.CTkFont(size=13, weight="bold" if is_selected else "normal"),
                corner_radius=8,
                command=lambda n=name: self.edit_template(n)
            )
            item_btn.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                item_frame,
                text="✕",
                width=32,
                height=32,
                fg_color="transparent",
                hover_color=COLOR_DANGER,
                text_color=COLOR_TEXT_DIM,
                font=ctk.CTkFont(size=14),
                corner_radius=6,
                command=lambda n=name: self.delete_template(n)
            )
            delete_btn.grid(row=0, column=1, padx=(0, 8), pady=4)
    
    def refresh_generator_menu(self):
        """Refresh the template dropdown in generator view."""
        template_names = list(self.templates.keys())
        self.template_menu.configure(values=template_names)
        
        if self.selected_template not in template_names and template_names:
            self.selected_template = template_names[0]
            self.template_var.set(self.selected_template)
        
        self.update_preview()
    
    def new_template(self):
        """Clear editor for new template."""
        self.editing_template = None
        self.editor_name_entry.delete(0, "end")
        self.editor_structure_textbox.delete("1.0", "end")
        self.update_editor_preview()
        self.refresh_template_list()
    
    def edit_template(self, name):
        """Load a template into the editor."""
        self.editing_template = name
        self.editor_name_entry.delete(0, "end")
        self.editor_name_entry.insert(0, name)
        
        formatted = format_paths_to_indented(self.templates[name])
        self.editor_structure_textbox.delete("1.0", "end")
        self.editor_structure_textbox.insert("1.0", formatted)
        
        self.update_editor_preview()
        self.refresh_template_list()
    
    def save_template(self):
        """Save the current template."""
        name = self.editor_name_entry.get().strip()
        content = self.editor_structure_textbox.get("1.0", "end").strip()
        
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a template name.")
            return
        
        if not content:
            messagebox.showwarning("Empty Structure", "Please define at least one folder.")
            return
        
        paths = parse_indented_lines(content)
        self.templates[name] = paths
        save_templates(self.templates)
        
        self.editing_template = name
        self.refresh_template_list()
        self.refresh_generator_menu()
        
        messagebox.showinfo("Saved! 💾", f"Template '{name}' has been saved.")
    
    def delete_template(self, name):
        """Delete a template."""
        if messagebox.askyesno("Delete Template?", f"Are you sure you want to delete '{name}'?\n\nThis cannot be undone."):
            if name in self.templates:
                del self.templates[name]
                save_templates(self.templates)
                
                if self.editing_template == name:
                    self.new_template()
                
                self.refresh_template_list()
                self.refresh_generator_menu()
    
    def update_editor_preview(self, event=None):
        """Update the live preview in editor."""
        content = self.editor_structure_textbox.get("1.0", "end").strip()
        if content:
            paths = parse_indented_lines(content)
            tree_text = format_paths_to_tree(paths)
        else:
            tree_text = "  Start typing to see preview..."
        
        self.editor_preview_textbox.configure(state="normal")
        self.editor_preview_textbox.delete("1.0", "end")
        self.editor_preview_textbox.insert("1.0", tree_text)
        self.editor_preview_textbox.configure(state="disabled")
    
    def export_template(self):
        """Export the current template to a JSON file."""
        name = self.editor_name_entry.get().strip()
        content = self.editor_structure_textbox.get("1.0", "end").strip()
        
        if not name:
            messagebox.showwarning("No Template", "Please enter a template name before exporting.")
            return
        
        if not content:
            messagebox.showwarning("Empty Template", "Please add some folders before exporting.")
            return
        
        # Parse structure
        paths = parse_indented_lines(content)
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Template",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile=f"{name.replace('/', '-')}.json"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Create export data
        export_data = {
            "template_name": name,
            "structure": paths
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Exported! 📤", f"Template '{name}' exported successfully!\n\nFile: {file_path}")
        except Exception as ex:
            messagebox.showerror("Export Failed", f"Could not export template:\n{ex}")
    
    def import_template(self):
        """Import a template from a JSON file."""
        file_path = filedialog.askopenfilename(
            title="Import Template",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate structure
            if "template_name" not in data or "structure" not in data:
                messagebox.showerror(
                    "Invalid File", 
                    "This file is not a valid FolderCrafter template.\n\n"
                    "Expected format:\n"
                    '{"template_name": "...", "structure": [...]}'
                )
                return
            
            name = data["template_name"]
            structure = data["structure"]
            
            # Validate structure is a list
            if not isinstance(structure, list):
                messagebox.showerror("Invalid Structure", "The 'structure' field must be a list of folder paths.")
                return
            
            # Handle name conflict
            original_name = name
            counter = 1
            while name in self.templates:
                name = f"{original_name} (Imported)"
                if counter > 1:
                    name = f"{original_name} (Imported {counter})"
                counter += 1
            
            # Save the template
            self.templates[name] = structure
            save_templates(self.templates)
            
            # Refresh UI
            self.refresh_template_list()
            self.refresh_generator_menu()
            
            # Load into editor
            self.edit_template(name)
            
            messagebox.showinfo("Imported! 📥", f"Template '{name}' imported successfully!")
            
        except json.JSONDecodeError:
            messagebox.showerror("Invalid JSON", "The file contains invalid JSON data.\n\nPlease check the file format.")
        except Exception as ex:
            messagebox.showerror("Import Failed", f"Could not import template:\n{ex}")


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    app = FolderCrafterApp()
    app.mainloop()
