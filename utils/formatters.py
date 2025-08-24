import json
import streamlit as st

def display_travel_state(file_path="artifacts/state.txt"):
    # Load state file
    with open(file_path, "r") as f:
        state = json.load(f)

    # 1. Attractions
    st.header("🌍 Attractions")
    for a in state.get("attractions", []):
        st.markdown(f"**{a['title']}** ({a.get('category','')})")
        st.write(f"⭐ {a.get('rating','N/A')} | 📍 {a.get('address','')}")
        if a.get("website"):
            st.markdown(f"[Website]({a['website']})")
        st.write("---")

    # 2. Weather
    st.header("⛅ Weather Forecast")
    for date, w in state.get("weather", {}).items():
        st.markdown(
            f"**{date}**: {w['condition']} "
            f"({w['min_temp']}°C - {w['max_temp']}°C, avg {w['avg_temp']}°C) "
            f"| 🌧️ {w['rain_prob']}% rain"
        )

    # 3. Filtered Attractions
    st.header("✅ Filtered Attractions (Weather Adjusted)")
    for a in state.get("filtered_attractions", []):
        st.markdown(f"**{a['title']}** - ⭐ {a['rating']}")

    # 4. Hotels
    st.header("🏨 Hotels")
    for h in state.get("hotels", []):
        st.markdown(f"**{h['name']}** ({h.get('category','')})")
        st.write(f"⭐ {h['rating']} ({h['rating_count']} reviews)")
        st.write(f"📍 {h['address']}")
        if h.get("website"):
            st.markdown(f"[Website]({h['website']})")
        st.write("---")

    # 5. Restaurants
    st.header("🍽️ Restaurants")
    for r in state.get("restaurants", []):
        st.markdown(f"**{r['name']}** ({r.get('category','')})")
        st.write(f"⭐ {r['rating']} ({r['rating_count']} reviews)")
        st.write(f"📍 {r['address']}")
        st.write(f"💲 {r.get('price_level','N/A')}")
        if r.get("website"):
            st.markdown(f"[Website]({r['website']})")
        st.write("---")

    # 6. Itinerary
    st.header("🗓️ Itinerary")
    st.markdown("\n".join(state.get("itinerary", [])))

    # 7. Exchange Rate
    st.header("💱 Currency Conversion")
    st.write(
        f"1 {state['user_input']['current_city']} currency ≈ "
        f"{state.get('exchange_value')} {state.get('to_currency','')}"
    )

    # 8. Summary
    st.header("📖 Trip Summary")
    st.markdown(state.get("summary",""), unsafe_allow_html=True)
