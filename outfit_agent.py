#!/usr/bin/env python3
"""
AI Outfit Stylist - Command Line Version
Helps you discover outfit ideas based on any clothing item you search for.
"""

import json
import os
import sys
import argparse

# Demo data for when no API key is available
DEMO_SUGGESTIONS = {
    "blue jeans": {
        "search_item_description": "Classic blue denim jeans - the ultimate wardrobe staple that pairs with virtually anything and transitions effortlessly from day to night.",
        "complete_outfits": [
            {
                "outfit_name": "Casual Cool",
                "description": "An effortlessly stylish everyday look that's perfect for running errands or grabbing coffee with friends.",
                "items": [
                    {"category": "tops", "item": "White Crew Neck T-Shirt", "details": "100% cotton, relaxed fit in crisp white", "why_it_works": "The classic white tee creates a clean, timeless contrast with blue denim"},
                    {"category": "shoes", "item": "White Leather Sneakers", "details": "Minimalist design, clean white leather", "why_it_works": "Keeps the look casual while adding a polished, fresh element"},
                    {"category": "accessories", "item": "Brown Leather Belt", "details": "Medium width, silver buckle", "why_it_works": "Adds a touch of sophistication and breaks up the blue-white palette"},
                    {"category": "outerwear", "item": "Denim Jacket (Light Wash)", "details": "Classic cut in a lighter shade than your jeans", "why_it_works": "Creates a Canadian tuxedo effect when done right with contrasting denim shades"}
                ],
                "styling_tips": "Cuff your jeans slightly to show off your sneakers and add visual interest. Tuck in the front of your t-shirt for a more intentional look."
            },
            {
                "outfit_name": "Smart Casual",
                "description": "Elevated denim styling perfect for a nice dinner or casual Friday at the office.",
                "items": [
                    {"category": "tops", "item": "Light Blue Oxford Shirt", "details": "Button-down collar, slim fit, cotton", "why_it_works": "The blue-on-blue creates a sophisticated tonal look"},
                    {"category": "shoes", "item": "Tan Suede Loafers", "details": "Penny loafer style in warm tan suede", "why_it_works": "Elevates the jeans while maintaining comfort and warmth in the color palette"},
                    {"category": "accessories", "item": "Leather Watch", "details": "Brown leather strap, classic dial", "why_it_works": "Adds a refined touch that signals attention to detail"},
                    {"category": "outerwear", "item": "Navy Blazer", "details": "Unstructured cotton blend, gold buttons", "why_it_works": "Instantly elevates any jeans outfit while staying comfortable"}
                ],
                "styling_tips": "Roll up your shirt sleeves once or twice for a relaxed vibe. Make sure your jeans are dark wash and well-fitted for this elevated look."
            },
            {
                "outfit_name": "Weekend Explorer",
                "description": "A rugged yet stylish outfit for outdoor adventures or weekend getaways.",
                "items": [
                    {"category": "tops", "item": "Flannel Shirt", "details": "Red and black buffalo check, brushed cotton", "why_it_works": "Adds texture and warmth while creating visual interest with the pattern"},
                    {"category": "shoes", "item": "Brown Leather Boots", "details": "Lace-up work boot style, Goodyear welted", "why_it_works": "Rugged durability that complements the casual, outdoorsy vibe"},
                    {"category": "accessories", "item": "Canvas Backpack", "details": "Waxed canvas in olive green", "why_it_works": "Functional and stylish, the earthy tone complements the warm flannel"},
                    {"category": "outerwear", "item": "Quilted Vest", "details": "Navy or olive, lightweight insulation", "why_it_works": "Adds warmth and layers without restricting movement"}
                ],
                "styling_tips": "Leave the flannel untucked and unbuttoned with a plain tee underneath. Cuff your jeans to show off your boots."
            }
        ],
        "color_palette": ["White", "Navy", "Tan/Camel", "Burgundy", "Forest Green", "Gray"],
        "avoid": ["Matching blue denim top (unless contrasting shades)", "Overly distressed pieces for formal settings", "Baggy fits that overwhelm your frame", "Clashing bold patterns"],
        "celebrity_inspiration": "Ryan Gosling - known for his effortless ability to dress up or down classic blue jeans with impeccable style",
        "pro_tip": "Invest in quality denim that fits perfectly. The right pair of jeans should hug your body without restricting movement, and the wash should be versatile enough to dress up or down."
    }
}

def get_demo_suggestions(item: str) -> dict:
    """Return demo suggestions for common items."""
    item_lower = item.lower()
    
    # Check for exact or partial matches
    for key in DEMO_SUGGESTIONS:
        if key in item_lower or item_lower in key:
            return DEMO_SUGGESTIONS[key]
    
    # Generic suggestions for any item
    return {
        "search_item_description": f"Your {item} - a versatile piece that can be styled in many creative ways!",
        "complete_outfits": [
            {
                "outfit_name": "Everyday Essential",
                "description": f"A balanced, go-to outfit featuring your {item} as the star piece.",
                "items": [
                    {"category": "tops", "item": "Neutral Basic Top", "details": "In white, black, or gray", "why_it_works": "Neutral colors let your statement piece shine"},
                    {"category": "bottoms", "item": "Well-Fitted Pants", "details": "Classic cut in a complementary color", "why_it_works": "Creates a balanced silhouette"},
                    {"category": "shoes", "item": "Versatile Footwear", "details": "Sneakers or loafers depending on occasion", "why_it_works": "Grounds the outfit appropriately"},
                    {"category": "accessories", "item": "Simple Accessories", "details": "Watch, belt, or minimal jewelry", "why_it_works": "Adds polish without competing for attention"}
                ],
                "styling_tips": "Keep the rest of your outfit simple to let your key piece stand out. Pay attention to proportion and balance."
            }
        ],
        "color_palette": ["White", "Black", "Navy", "Gray", "Beige"],
        "avoid": ["Competing statement pieces", "Clashing colors", "Over-accessorizing"],
        "celebrity_inspiration": "Timeless style icons who master the art of simple, elegant dressing",
        "pro_tip": "The key to great style is confidence. Wear what makes you feel good and own it!"
    }


def get_outfit_suggestions(item: str, style: str = "Classic & Timeless", 
                          occasion: str = "Everyday Casual", season: str = "Year-Round",
                          api_key: str = None, use_demo: bool = False):
    """Generate outfit suggestions using OpenAI API or demo data."""
    
    if use_demo:
        return get_demo_suggestions(item)
    
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print_colored("\n⚠️  No OpenAI API key found. Running in DEMO mode...", "yellow", bold=True)
        return get_demo_suggestions(item)
    
    try:
        import openai
    except ImportError:
        print("Installing openai package...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai", "-q"])
        import openai
    
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""You are an expert fashion stylist and personal shopper. A customer is looking for outfit ideas based on a specific clothing item they're interested in.

The customer searched for: "{item}"
Style preference: {style}
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

Provide 3 different complete outfit suggestions, ranging from casual to more dressed up. Be specific with item recommendations."""

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
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()
    
    return json.loads(content)


def print_colored(text: str, color: str = "white", bold: bool = False):
    """Print colored text to terminal."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    bold_code = "\033[1m" if bold else ""
    print(f"{bold_code}{colors.get(color, '')}{text}{colors['reset']}")


def print_separator(char: str = "─", length: int = 70):
    """Print a separator line."""
    print_colored(char * length, "cyan")


def display_suggestions(suggestions: dict, search_item: str):
    """Display outfit suggestions in a beautiful terminal format."""
    
    print("\n")
    print_separator("═")
    print_colored(f"  👗 AI OUTFIT STYLIST - Results for: {search_item.upper()}", "magenta", bold=True)
    print_separator("═")
    
    # Item description
    print_colored(f"\n📝 {suggestions.get('search_item_description', '')}", "white")
    
    # Color palette
    if 'color_palette' in suggestions:
        print_colored("\n🎨 COMPLEMENTARY COLORS:", "yellow", bold=True)
        colors = " | ".join(suggestions['color_palette'])
        print_colored(f"   {colors}", "white")
    
    # Complete outfits
    print_colored("\n" + "─" * 70, "cyan")
    print_colored("👔 COMPLETE OUTFIT IDEAS", "green", bold=True)
    print_colored("─" * 70, "cyan")
    
    for i, outfit in enumerate(suggestions.get('complete_outfits', []), 1):
        print_colored(f"\n✨ LOOK {i}: {outfit['outfit_name']}", "magenta", bold=True)
        print_colored(f"   {outfit['description']}", "white")
        
        print_colored("\n   Items:", "cyan", bold=True)
        for item in outfit['items']:
            category_icons = {
                "tops": "👕",
                "bottoms": "👖",
                "shoes": "👟",
                "accessories": "👜",
                "outerwear": "🧥"
            }
            icon = category_icons.get(item['category'].lower(), "•")
            print_colored(f"\n   {icon} [{item['category'].upper()}] {item['item']}", "yellow")
            print_colored(f"      {item['details']}", "white")
            print_colored(f"      💡 {item['why_it_works']}", "cyan")
        
        print_colored(f"\n   👠 Styling Tip: {outfit['styling_tips']}", "green")
        print_separator("─")
    
    # What to avoid
    if 'avoid' in suggestions:
        print_colored("\n🚫 WHAT TO AVOID:", "red", bold=True)
        for item in suggestions['avoid']:
            print_colored(f"   • {item}", "white")
    
    # Celebrity inspiration
    if 'celebrity_inspiration' in suggestions:
        print_colored(f"\n🌟 STYLE INSPIRATION: {suggestions['celebrity_inspiration']}", "yellow")
    
    # Pro tip
    if 'pro_tip' in suggestions:
        print_colored("\n💎 PRO STYLIST TIP:", "green", bold=True)
        print_colored(f"   {suggestions['pro_tip']}", "white")
    
    print("\n")
    print_separator("═")
    print_colored("  Made with ❤️  by AI Outfit Stylist | Powered by OpenAI", "cyan")
    print_separator("═")
    print("\n")


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="👗 AI Outfit Stylist - Get outfit suggestions for any clothing item",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python outfit_agent.py --search "blue jeans"
  python outfit_agent.py --search "white sneakers" --style "Trendy & Fashion-Forward"
  python outfit_agent.py --search "leather jacket" --occasion "Date Night"
  python outfit_agent.py --demo --search "blue jeans"  (runs with sample data)
        """
    )
    
    parser.add_argument("--search", "-s", type=str, help="Clothing item to search for", default="blue jeans")
    parser.add_argument("--style", type=str, default="Classic & Timeless",
                       choices=["Classic & Timeless", "Trendy & Fashion-Forward", 
                               "Casual & Relaxed", "Minimalist & Clean", "Bold & Eclectic"],
                       help="Style preference")
    parser.add_argument("--occasion", "-o", type=str, default="Everyday Casual",
                       choices=["Everyday Casual", "Work/Office", "Date Night", 
                               "Weekend Brunch", "Special Event"],
                       help="Occasion for the outfit")
    parser.add_argument("--season", type=str, default="Year-Round",
                       choices=["Spring", "Summer", "Fall/Autumn", "Winter", "Year-Round"],
                       help="Season for the outfit")
    parser.add_argument("--api-key", type=str, help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--demo", "-d", action="store_true", 
                       help="Run in demo mode with sample data (no API key needed)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    
    print_colored("\n" + "═" * 70, "magenta")
    print_colored("        👗 AI OUTFIT STYLIST - Your Personal Fashion Agent", "magenta", bold=True)
    print_colored("═" * 70, "magenta")
    
    if args.demo:
        print_colored("\n🎭 Running in DEMO mode with sample data", "yellow", bold=True)
    
    print_colored(f"\n🔍 Searching for: {args.search}", "yellow", bold=True)
    print_colored(f"   Style: {args.style}", "white")
    print_colored(f"   Occasion: {args.occasion} | Season: {args.season}", "white")
    print_colored("\n⏳ Our AI stylist is curating the perfect outfits for you...", "cyan", bold=True)
    
    try:
        suggestions = get_outfit_suggestions(
            args.search, args.style, args.occasion, args.season, 
            api_key, use_demo=args.demo
        )
        if suggestions:
            display_suggestions(suggestions, args.search)
    except Exception as e:
        print_colored(f"\n❌ Error: {str(e)}", "red")
        print_colored("Falling back to demo mode...", "yellow")
        suggestions = get_demo_suggestions(args.search)
        display_suggestions(suggestions, args.search)


if __name__ == "__main__":
    main()
