import streamlit as st
import openai
import json
import os
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="AI Outfit Stylist",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, beautiful UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Search container */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Outfit card styling */
    .outfit-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .outfit-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .outfit-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .outfit-description {
        color: #666;
        line-height: 1.6;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-tops { background: #e3f2fd; color: #1565c0; }
    .badge-bottoms { background: #f3e5f5; color: #7b1fa2; }
    .badge-shoes { background: #fff3e0; color: #ef6c00; }
    .badge-accessories { background: #e8f5e9; color: #2e7d32; }
    .badge-outerwear { background: #fce4ec; color: #c2185b; }
    
    /* Tips section */
    .style-tip {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        border-left: 4px solid #fbc02d;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 30px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def get_outfit_suggestions(item: str, style_preference: str, occasion: str, season: str, api_key: str) -> Optional[dict]:
    """Generate outfit suggestions using OpenAI API."""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""You are an expert fashion stylist and personal shopper. A customer is looking for outfit ideas based on a specific clothing item they're interested in.

The customer searched for: "{item}"
Style preference: {style_preference}
Occasion: {occasion}
Season: {season}

Please provide comprehensive outfit suggestions in the following JSON format:
{{
    "search_item_description": "A brief, stylish description of the searched item",
    "complete_outfits": [
        {{
            "outfit_name": "Creative name for this complete look",
            "description": "Description of the overall look and vibe",
            "items": [
                {{
                    "category": "tops/bottoms/shoes/accessories/outerwear",
                    "item": "Specific item name",
                    "details": "Color, material, style details",
                    "why_it_works": "Brief explanation of why this pairs well"
                }}
            ],
            "styling_tips": "How to style this outfit for the best look"
        }}
    ],
    "color_palette": ["List of colors that complement the searched item"],
    "avoid": ["Things to avoid pairing with this item"],
    "celebrity_inspiration": "A celebrity or style icon known for wearing similar looks",
    "pro_tip": "An expert styling tip for this type of item"
}}

Provide 3 different complete outfit suggestions, ranging from casual to more dressed up. Be specific with item recommendations and include a good mix of accessible and aspirational pieces."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert fashion stylist. Always respond with valid JSON only, no additional text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        return json.loads(content)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing AI response. Please try again.")
        return None
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None


def display_outfit_card(outfit: dict, index: int):
    """Display a single outfit suggestion card."""
    colors = ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"]
    color = colors[index % len(colors)]
    
    st.markdown(f"""
    <div class="outfit-card" style="border-left-color: {color};">
        <div class="outfit-title">✨ {outfit['outfit_name']}</div>
        <div class="outfit-description">{outfit['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display items in columns
    cols = st.columns(min(len(outfit['items']), 3))
    for i, item in enumerate(outfit['items']):
        with cols[i % 3]:
            category = item['category'].lower()
            badge_class = f"badge-{category}" if category in ['tops', 'bottoms', 'shoes', 'accessories', 'outerwear'] else "badge-accessories"
            
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 12px; margin-bottom: 0.5rem; height: 100%;">
                <span class="category-badge {badge_class}">{item['category'].upper()}</span>
                <h4 style="margin: 0.5rem 0; color: #333;">{item['item']}</h4>
                <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">{item['details']}</p>
                <p style="color: #888; font-size: 0.85rem; font-style: italic;">💡 {item['why_it_works']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Styling tips
    st.markdown(f"""
    <div class="style-tip">
        <strong>👠 Styling Tip:</strong> {outfit['styling_tips']}
    </div>
    """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👗 AI Outfit Stylist</h1>
        <p>Your personal AI-powered fashion advisor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to power the AI suggestions",
            placeholder="sk-..."
        )
        
        # Check for API key in environment
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY", "")
        
        st.markdown("---")
        st.markdown("### 🎨 Style Preferences")
        
        style_preference = st.selectbox(
            "Your Style",
            ["Classic & Timeless", "Trendy & Fashion-Forward", "Casual & Relaxed", 
             "Minimalist & Clean", "Bold & Eclectic", "Bohemian & Free-Spirited",
             "Sporty & Athletic", "Elegant & Sophisticated"]
        )
        
        occasion = st.selectbox(
            "Occasion",
            ["Everyday Casual", "Work/Office", "Date Night", "Weekend Brunch",
             "Special Event", "Vacation", "Night Out", "Job Interview"]
        )
        
        season = st.selectbox(
            "Season",
            ["Spring", "Summer", "Fall/Autumn", "Winter", "Year-Round"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### 💡 How to Use
        1. Enter your OpenAI API key
        2. Select your style preferences
        3. Search for any clothing item
        4. Get personalized outfit ideas!
        
        ---
        
        ### 🌟 Example Searches
        - Blue jeans
        - White sneakers
        - Black blazer
        - Floral summer dress
        - Leather jacket
        - Beige trench coat
        """)
    
    # Main search area
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("### 🔍 What are you looking for?")
        search_item = st.text_input(
            "",
            placeholder="e.g., Blue jeans, white sneakers, floral dress...",
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            search_button = st.button("✨ Get Outfit Ideas", use_container_width=True)
    
    # Process search
    if search_button:
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key in the sidebar to get outfit suggestions.")
        elif not search_item:
            st.warning("⚠️ Please enter a clothing item to search for.")
        else:
            with st.spinner("🎨 Our AI stylist is curating the perfect outfits for you..."):
                suggestions = get_outfit_suggestions(
                    search_item, style_preference, occasion, season, api_key
                )
            
            if suggestions:
                st.markdown("---")
                
                # Item description
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 16px; color: white; margin-bottom: 2rem;">
                    <h2 style="margin: 0;">🛍️ {search_item.title()}</h2>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{suggestions.get('search_item_description', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Color palette
                if 'color_palette' in suggestions:
                    st.markdown("### 🎨 Complementary Colors")
                    color_cols = st.columns(len(suggestions['color_palette']))
                    for i, color in enumerate(suggestions['color_palette']):
                        with color_cols[i]:
                            st.markdown(f"""
                            <div style="background: #f0f0f0; padding: 0.8rem; border-radius: 10px; text-align: center;">
                                <span style="font-weight: 500;">{color}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Complete outfits
                st.markdown("### 👗 Complete Outfit Ideas")
                
                for i, outfit in enumerate(suggestions.get('complete_outfits', [])):
                    with st.expander(f"Look {i+1}: {outfit['outfit_name']}", expanded=(i==0)):
                        display_outfit_card(outfit, i)
                
                st.markdown("---")
                
                # Additional tips
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🚫 What to Avoid")
                    for item in suggestions.get('avoid', []):
                        st.markdown(f"- {item}")
                
                with col2:
                    st.markdown("### 🌟 Style Inspiration")
                    if 'celebrity_inspiration' in suggestions:
                        st.markdown(f"**Celebrity Inspo:** {suggestions['celebrity_inspiration']}")
                
                # Pro tip
                if 'pro_tip' in suggestions:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                                padding: 1.5rem; border-radius: 16px; color: white; margin-top: 1rem;">
                        <h4 style="margin: 0;">💎 Pro Stylist Tip</h4>
                        <p style="margin: 0.5rem 0 0 0;">{suggestions['pro_tip']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #888;">
        <p>Made with ❤️ by AI Outfit Stylist | Powered by OpenAI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
