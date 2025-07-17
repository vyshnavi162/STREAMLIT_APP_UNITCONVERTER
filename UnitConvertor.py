import streamlit as st
import math
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for history
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

# Conversion definitions
CONVERSION_CATEGORIES = {
    "📏 Length": {
        "Millimeter (mm)": 0.001,
        "Centimeter (cm)": 0.01,
        "Meter (m)": 1.0,
        "Kilometer (km)": 1000.0,
        "Inch (in)": 0.0254,
        "Foot (ft)": 0.3048,
        "Yard (yd)": 0.9144,
        "Mile (mi)": 1609.344,
        "Nautical Mile (nmi)": 1852.0
    },
    "⚖️ Weight": {
        "Milligram (mg)": 0.000001,
        "Gram (g)": 0.001,
        "Kilogram (kg)": 1.0,
        "Ton (t)": 1000.0,
        "Ounce (oz)": 0.0283495,
        "Pound (lb)": 0.453592,
        "Stone (st)": 6.35029
    },
    "🌡️ Temperature": {
        "Celsius (°C)": "celsius",
        "Fahrenheit (°F)": "fahrenheit",
        "Kelvin (K)": "kelvin",
        "Rankine (°R)": "rankine"
    },
    "💧 Volume": {
        "Milliliter (ml)": 0.001,
        "Liter (l)": 1.0,
        "Cubic Meter (m³)": 1000.0,
        "Fluid Ounce (fl oz)": 0.0295735,
        "Cup (cup)": 0.236588,
        "Pint (pt)": 0.473176,
        "Quart (qt)": 0.946353,
        "Gallon (gal)": 3.78541,
        "Cubic Inch (in³)": 0.0163871,
        "Cubic Foot (ft³)": 28.3168
    },
    "📐 Area": {
        "Square Millimeter (mm²)": 0.000001,
        "Square Centimeter (cm²)": 0.0001,
        "Square Meter (m²)": 1.0,
        "Square Kilometer (km²)": 1000000.0,
        "Square Inch (in²)": 0.00064516,
        "Square Foot (ft²)": 0.092903,
        "Square Yard (yd²)": 0.836127,
        "Acre (ac)": 4046.86,
        "Hectare (ha)": 10000.0
    },
    "⚡ Energy": {
        "Joule (J)": 1.0,
        "Kilojoule (kJ)": 1000.0,
        "Calorie (cal)": 4.184,
        "Kilocalorie (kcal)": 4184.0,
        "Watt-hour (Wh)": 3600.0,
        "Kilowatt-hour (kWh)": 3600000.0,
        "BTU": 1055.06,
        "Electronvolt (eV)": 1.602176634e-19
    },
    "💨 Speed": {
        "Meter per Second (m/s)": 1.0,
        "Kilometer per Hour (km/h)": 0.277778,
        "Mile per Hour (mph)": 0.44704,
        "Foot per Second (ft/s)": 0.3048,
        "Knot (kt)": 0.514444,
        "Mach": 343.0
    },
    "⏱️ Time": {
        "Millisecond (ms)": 0.001,
        "Second (s)": 1.0,
        "Minute (min)": 60.0,
        "Hour (h)": 3600.0,
        "Day (d)": 86400.0,
        "Week (wk)": 604800.0,
        "Month (mo)": 2629746.0,
        "Year (yr)": 31556952.0
    },
    "💾 Digital Storage": {
        "Bit (b)": 1.0,
        "Byte (B)": 8.0,
        "Kilobyte (KB)": 8000.0,
        "Megabyte (MB)": 8000000.0,
        "Gigabyte (GB)": 8000000000.0,
        "Terabyte (TB)": 8000000000000.0,
        "Petabyte (PB)": 8000000000000000.0,
        "Kibibyte (KiB)": 8192.0,
        "Mebibyte (MiB)": 8388608.0,
        "Gibibyte (GiB)": 8589934592.0,
        "Tebibyte (TiB)": 8796093022208.0
    }
}

# Temperature conversion functions
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def celsius_to_rankine(celsius):
    return (celsius + 273.15) * 9/5

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def rankine_to_celsius(rankine):
    return (rankine * 5/9) - 273.15

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between different units"""
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = fahrenheit_to_celsius(value)
    elif from_unit == "kelvin":
        celsius = kelvin_to_celsius(value)
    elif from_unit == "rankine":
        celsius = rankine_to_celsius(value)
    
    # Convert from Celsius to target unit
    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return celsius_to_fahrenheit(celsius)
    elif to_unit == "kelvin":
        return celsius_to_kelvin(celsius)
    elif to_unit == "rankine":
        return celsius_to_rankine(celsius)

def convert_units(value, from_unit, to_unit, category):
    """Convert between units within the same category"""
    if category == "🌡️ Temperature":
        from_key = CONVERSION_CATEGORIES[category][from_unit]
        to_key = CONVERSION_CATEGORIES[category][to_unit]
        return convert_temperature(value, from_key, to_key)
    else:
        # For other categories, use multiplication factors
        from_factor = CONVERSION_CATEGORIES[category][from_unit]
        to_factor = CONVERSION_CATEGORIES[category][to_unit]
        return value * from_factor / to_factor

def add_to_history(category, value, from_unit, to_unit, result):
    """Add conversion to history"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    history_entry = {
        "timestamp": timestamp,
        "category": category,
        "conversion": f"{value} {from_unit} = {result:.6f} {to_unit}"
    }
    st.session_state.conversion_history.insert(0, history_entry)
    # Keep only last 10 conversions
    if len(st.session_state.conversion_history) > 10:
        st.session_state.conversion_history.pop()

def main():
    st.title("🔄 Universal Unit Converter")
    st.markdown("Convert between various units of measurement with ease!")
    
    # Sidebar for category selection and history
    with st.sidebar:
        st.header("🎯 Categories")
        
        # Category selection
        selected_category = st.selectbox(
            "Choose conversion category:",
            options=list(CONVERSION_CATEGORIES.keys()),
            key="category_selector"
        )
        
        st.divider()
        
        # Quick conversion buttons
        st.header("⚡ Quick Conversions")
        quick_conversions = {
            "°C to °F": ("🌡️ Temperature", "Celsius (°C)", "Fahrenheit (°F)"),
            "ft to m": ("📏 Length", "Foot (ft)", "Meter (m)"),
            "lb to kg": ("⚖️ Weight", "Pound (lb)", "Kilogram (kg)"),
            "gal to L": ("💧 Volume", "Gallon (gal)", "Liter (l)"),
            "mph to km/h": ("💨 Speed", "Mile per Hour (mph)", "Kilometer per Hour (km/h)")
        }
        
        for button_text, (cat, from_u, to_u) in quick_conversions.items():
            if st.button(button_text, use_container_width=True):
                st.session_state.category_selector = cat
                st.session_state.from_unit = from_u
                st.session_state.to_unit = to_u
                st.experimental_rerun()
        
        st.divider()
        
        # Conversion history
        st.header("📚 Recent Conversions")
        if st.session_state.conversion_history:
            for entry in st.session_state.conversion_history:
                st.caption(f"**{entry['timestamp']}**")
                st.write(entry['conversion'])
                st.caption(f"*{entry['category']}*")
                st.markdown("---")
        else:
            st.info("No conversions yet!")
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.conversion_history = []
            st.experimental_rerun()
    
    # Main conversion interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 From")
        
        # Input value
        input_value = st.number_input(
            "Enter value to convert:",
            value=1.0,
            format="%.6f",
            key="input_value"
        )
        
        # From unit selection
        from_unit = st.selectbox(
            "From unit:",
            options=list(CONVERSION_CATEGORIES[selected_category].keys()),
            key="from_unit"
        )
    
    with col2:
        st.subheader("📤 To")
        
        # To unit selection
        to_unit = st.selectbox(
            "To unit:",
            options=list(CONVERSION_CATEGORIES[selected_category].keys()),
            key="to_unit"
        )
        
        # Result display
        try:
            result = convert_units(input_value, from_unit, to_unit, selected_category)
            st.metric(
                label="Converted value:",
                value=f"{result:.6f}",
                delta=None
            )
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")
            result = None
    
    # Convert button
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔄 Convert", type="primary", use_container_width=True):
            if result is not None:
                add_to_history(selected_category, input_value, from_unit, to_unit, result)
                st.success(f"✅ {input_value} {from_unit} = {result:.6f} {to_unit}")
                st.balloons()
    
    # Swap units button
    with col3:
        if st.button("🔄 Swap Units", use_container_width=True):
            # Swap the units
            temp_from = st.session_state.from_unit
            st.session_state.from_unit = st.session_state.to_unit
            st.session_state.to_unit = temp_from
            st.experimental_rerun()
    
    # Information section
    st.divider()
    
    # Category information
    with st.expander(f"ℹ️ About {selected_category}"):
        if selected_category == "🌡️ Temperature":
            st.markdown("""
            **Temperature Conversion:**
            - **Celsius (°C)**: Water freezes at 0°C, boils at 100°C
            - **Fahrenheit (°F)**: Water freezes at 32°F, boils at 212°F
            - **Kelvin (K)**: Absolute temperature scale, 0K = -273.15°C
            - **Rankine (°R)**: Absolute Fahrenheit scale, 0°R = -459.67°F
            """)
        elif selected_category == "📏 Length":
            st.markdown("""
            **Length Conversion:**
            - **Metric**: mm, cm, m, km
            - **Imperial**: in, ft, yd, mi
            - **Special**: Nautical miles for navigation
            """)
        elif selected_category == "⚖️ Weight":
            st.markdown("""
            **Weight/Mass Conversion:**
            - **Metric**: mg, g, kg, t (metric tons)
            - **Imperial**: oz, lb, st (stones)
            """)
        elif selected_category == "💧 Volume":
            st.markdown("""
            **Volume Conversion:**
            - **Metric**: ml, l, m³
            - **Imperial**: fl oz, cup, pt, qt, gal
            - **Cubic**: in³, ft³
            """)
        elif selected_category == "💾 Digital Storage":
            st.markdown("""
            **Digital Storage:**
            - **Decimal**: KB, MB, GB, TB (base 1000)
            - **Binary**: KiB, MiB, GiB, TiB (base 1024)
            - **Basic**: Bits and Bytes
            """)
    
    # Tips section
    with st.expander("💡 Tips & Tricks"):
        st.markdown("""
        ### 🎯 Pro Tips:
        - **Use Quick Conversions** in the sidebar for common conversions
        - **Check History** to see your recent conversions
        - **Swap Units** button quickly reverses the conversion direction
        - **High Precision** - Results shown to 6 decimal places
        - **Real-time Updates** - Results update as you type
        
        ### 🔧 Features:
        - **8 Categories** covering most common conversion needs
        - **50+ Units** across all categories
        - **Temperature Handling** with proper formula conversions
        - **Conversion History** keeps track of recent calculations
        - **Responsive Design** works on all screen sizes
        """)

if __name__ == "__main__":
    main()