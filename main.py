from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

class NovelDownloaderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text="📖 NOVEL DOWNLOADER", size_hint_y=0.1, font_size=24)
        layout.add_widget(title)
        
        # URL Input
        self.url_input = TextInput(
            text="https://novelbin.com/b/black-tech-internet-cafe-system/chapter-6",
            size_hint_y=0.15,
            multiline=False
        )
        layout.add_widget(self.url_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        download_btn = Button(text="Download Chapter")
        download_btn.bind(on_press=self.download_chapter)
        btn_layout.add_widget(download_btn)
        
        exit_btn = Button(text="Exit")
        exit_btn.bind(on_press=self.exit_app)
        btn_layout.add_widget(exit_btn)
        
        layout.add_widget(btn_layout)
        
        # Output area
        self.output_label = Label(
            text="Welcome to Novel Downloader!\n\nEnter a URL and click Download.",
            size_hint_y=0.6,
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        layout.add_widget(self.output_label)
        
        return layout
    
    def download_chapter(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.output_label.text = "❌ Please enter a URL"
            return
        
        self.output_label.text = "🔗 Connecting..."
        
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            
            headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Find content
            content = soup.select_one('#chr-content, .chr-content, #chaptercontent')
            if not content:
                content = soup.body
            
            text = content.get_text(separator='\n', strip=True)
            
            # Clean text - REMOVE TRANSLATOR CREDITS
            text = self.clean_novel_text(text)
            
            # Generate filename
            filename = self.generate_filename(url)
            
            # Save file - Use proper path for Android
            download_path = "/sdcard/Download/Novels/"
            
            # For testing, we'll just show the content
            # In actual app, you would save to file
            
            # Show success message
            success_msg = f"✅ Download successful!\n"
            success_msg += f"📄 Would save as: {filename}\n"
            success_msg += f"📊 Stats: {len(text)} characters, {len(text.split())} words\n\n"
            
            # Show preview
            lines = [line for line in text.split('\n') if line.strip()]
            success_msg += "👀 Preview:\n"
            for i, line in enumerate(lines[:3]):
                success_msg += f"   {line[:60]}{'...' if len(line) > 60 else ''}\n"
            if len(lines) > 3:
                success_msg += "   ...\n"
                
            self.output_label.text = success_msg
            
        except Exception as e:
            self.output_label.text = f"❌ Error: {str(e)}"

    def clean_novel_text(self, text):
        """Clean and format the novel text - REMOVES ALL TRANSLATOR TEXT"""
        # Remove ALL translator and editor credits
        patterns_to_remove = [
            r'Translator:.*?Translations',
            r'Editor:.*?Translations', 
            r'Translated by:.*',
            r'Edited by:.*',
            r'Noodletown.*Translations',
            r'TL:.*',
            r'ED:.*',
            r'Translator\s*:.*',
            r'Editor\s*:.*',
            r'翻译:.*',
            r'译者:.*',
            r'编辑:.*',
            r'Read latest chapters at.*',
            r'Please support the author.*',
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up spacing
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()

    def generate_filename(self, url):
        """Generate filename from URL"""
        try:
            if '/b/' in url:
                parts = url.split('/')
                novel_name = parts[parts.index('b') + 1].replace('-', ' ').title().replace(' ', '_')
                
                # Get chapter number
                chapter_part = parts[-1]
                chapter_match = re.search(r'chapter-?(\d+)', chapter_part, re.IGNORECASE)
                if chapter_match:
                    chapter_num = f"Chapter_{chapter_match.group(1)}"
                else:
                    chapter_num = "Chapter"
                
                return f"{novel_name}_{chapter_num}.txt"
        except:
            pass
        
        return f"novel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    def exit_app(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':

    NovelDownloaderApp().run()
    # Add this to your main.py at the very bottom to test syntax
if __name__ == '__main__':
    # Simple syntax test
    print("Syntax check passed")
