# 👗 AI Outfit Stylist

An intelligent, AI-powered outfit suggestion agent that helps you discover the perfect outfit combinations based on any clothing item you search for.

## ✨ Features

- **Smart Outfit Suggestions**: Get complete outfit ideas for any clothing item you search
- **Personalized Recommendations**: Customize suggestions based on style preference, occasion, and season
- **Complete Look Breakdowns**: Each outfit includes tops, bottoms, shoes, accessories, and outerwear
- **Color Palette Guidance**: Discover colors that complement your searched item
- **Styling Tips**: Expert advice on how to wear and style each outfit
- **Celebrity Inspiration**: Get inspired by style icons who rock similar looks
- **What to Avoid**: Learn what not to pair with your item

## 🚀 Quick Start

### Command Line Tool (Recommended)

Run the outfit agent directly from the terminal:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with demo data (no API key needed)
python outfit_agent.py --demo --search "blue jeans"

# Run with OpenAI API (for real AI suggestions)
export OPENAI_API_KEY="your-api-key"
python outfit_agent.py --search "blue jeans"
```

### Command Line Options

```bash
python outfit_agent.py --help

Options:
  --search, -s     Clothing item to search for (default: "blue jeans")
  --style          Style preference (Classic, Trendy, Casual, Minimalist, Bold)
  --occasion, -o   Occasion (Everyday, Work, Date Night, Brunch, Special Event)
  --season         Season (Spring, Summer, Fall, Winter, Year-Round)
  --api-key        OpenAI API key (or set OPENAI_API_KEY env var)
  --demo, -d       Run with sample data (no API key needed)
```

### Examples

```bash
# Search for blue jeans with casual style
python outfit_agent.py --search "blue jeans" --style "Casual & Relaxed"

# Search for white sneakers for a date night
python outfit_agent.py --search "white sneakers" --occasion "Date Night"

# Search for a leather jacket in winter
python outfit_agent.py --search "leather jacket" --season "Winter"
```

## 🌐 Web App (Streamlit)

You can also run the web interface:

```bash
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

## 📝 Example Output

When you search for "blue jeans", you'll get:

- **3 Complete Outfit Looks** (Casual Cool, Smart Casual, Weekend Explorer)
- **Complementary Colors** (White, Navy, Tan, Burgundy, Forest Green, Gray)
- **Detailed Item Recommendations** with specific styling tips
- **Celebrity Inspiration** (e.g., Ryan Gosling's effortless denim style)
- **Pro Stylist Tips** for making the most of your piece

## 🛠️ Tech Stack

- **AI Engine**: OpenAI GPT-4o
- **CLI Interface**: Python with colorful terminal output
- **Web Interface**: Streamlit with custom CSS
- **Language**: Python 3.8+

## 📄 Files

- `outfit_agent.py` - Command line outfit stylist
- `streamlit_app.py` - Web-based interface
- `requirements.txt` - Python dependencies

## 📄 License

This project is open source and available under the MIT License.

---

Made with ❤️ by AI Outfit Stylist | Powered by OpenAI
