import { useState } from "react";

const palette = {
  earth1: "#3B2A1A",
  earth2: "#6B4423",
  earth3: "#A0622B",
  earth4: "#C8843C",
  earth5: "#E8A855",
  sand1: "#F5EDD8",
  sand2: "#EDD9B0",
  sand3: "#D4B483",
  forest1: "#1E3A20",
  forest2: "#2D5A30",
  forest3: "#4A8050",
  forest4: "#7AB87A",
  clay: "#C4603A",
  terracotta: "#C0522A",
  cream: "#FAF3E6",
  accent: "#E84A2F",
};

const tribalArt = `
  <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" opacity="0.08">
    <defs>
      <pattern id="tribal" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
        <circle cx="30" cy="30" r="2" fill="#3B2A1A"/>
        <circle cx="10" cy="10" r="1.5" fill="#3B2A1A"/>
        <circle cx="50" cy="10" r="1.5" fill="#3B2A1A"/>
        <circle cx="10" cy="50" r="1.5" fill="#3B2A1A"/>
        <circle cx="50" cy="50" r="1.5" fill="#3B2A1A"/>
        <line x1="10" y1="10" x2="30" y2="30" stroke="#3B2A1A" strokeWidth="0.5"/>
        <line x1="50" y1="10" x2="30" y2="30" stroke="#3B2A1A" strokeWidth="0.5"/>
        <line x1="10" y1="50" x2="30" y2="30" stroke="#3B2A1A" strokeWidth="0.5"/>
        <line x1="50" y1="50" x2="30" y2="30" stroke="#3B2A1A" strokeWidth="0.5"/>
        <polygon points="30,15 35,25 25,25" fill="none" stroke="#3B2A1A" strokeWidth="0.5"/>
        <polygon points="30,45 35,35 25,35" fill="none" stroke="#3B2A1A" strokeWidth="0.5"/>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#tribal)"/>
  </svg>
`;

const homestays = [
  {
    id: 1, name: "Santal Tribal Eco Stay", owner: "Birsa Munda Family", village: "Deoghar Village", district: "Deoghar",
    tribe: "Santhal", price: 850, rating: 4.8, reviews: 32, image: "🏡",
    facilities: ["Home-cooked meals", "Folk dance shows", "Bonfire nights", "Village walks"],
    food: ["Dhuska", "Chilka Roti", "Thekua", "Mahua brew"],
    description: "Live with the Santal community in a traditional mud-and-thatch home. Wake up to forest birdsong and participate in daily village life.",
    available: true, category: "Tribal Stay"
  },
  {
    id: 2, name: "Bamboo Forest Cottage", owner: "Oraon Cooperative", village: "Netarhat Hills", district: "Latehar",
    tribe: "Oraon", price: 1100, rating: 4.9, reviews: 47, image: "🎋",
    facilities: ["Forest trek guide", "Waterfall visit", "Organic farm stay", "Traditional music"],
    food: ["Bamboo Chicken", "Rugra mushroom", "Forest rice", "Pitha"],
    description: "Nestled in the Queen of Jharkhand hills. Bamboo-built eco cottage with stunning sunrise views over Netarhat plateau.",
    available: true, category: "Eco Cottage"
  },
  {
    id: 3, name: "Munda Heritage Home", owner: "Sukra Munda & Family", village: "Khunti Town", district: "Khunti",
    tribe: "Munda", price: 700, rating: 4.6, reviews: 28, image: "🏠",
    facilities: ["Handloom weaving", "Pottery workshop", "Cultural ceremonies", "Local market visit"],
    food: ["Rice beer (Handia)", "Traditional pitha", "Wild greens curry", "Marka saag"],
    description: "Stay in the heartland of Munda culture. Learn handloom weaving and participate in the vibrant Sarhul festival if you time it right.",
    available: true, category: "Heritage Stay"
  },
  {
    id: 4, name: "Ho Tribal Jungle Camp", owner: "Ho Community Trust", village: "Chaibasa Forest", district: "West Singhbhum",
    tribe: "Ho", price: 950, rating: 4.7, reviews: 19, image: "⛺",
    facilities: ["Jungle safari", "River fishing", "Traditional archery", "Night sky watching"],
    food: ["Jungle herbs", "Fish curry", "Maize flatbread", "Wild tuber dishes"],
    description: "Immersive jungle camp experience with the Ho tribe. Learn traditional forest survival and witness the Maghe festival.",
    available: false, category: "Jungle Camp"
  },
  {
    id: 5, name: "Kharia Village Retreat", owner: "Kharia Women's SHG", village: "Simdega Hills", district: "Simdega",
    tribe: "Kharia", price: 800, rating: 4.5, reviews: 23, image: "🌿",
    facilities: ["Organic farming", "Basket weaving", "Traditional medicine walk", "Cooking class"],
    food: ["Chilka Roti", "Seasonal vegetables", "Rice preparations", "Local honey"],
    description: "Run entirely by Kharia women, this retreat offers deep immersion in hill tribal life, crafts, and sustainable forest practices.",
    available: true, category: "Women-led Stay"
  },
  {
    id: 6, name: "Birhor Forest Dwelling", owner: "Birhor Community", village: "Hazaribagh Forest", district: "Hazaribagh",
    tribe: "Birhor", price: 600, rating: 4.4, reviews: 11, image: "🌲",
    facilities: ["Rope-making demo", "Forest walk", "Story sessions", "Campfire cooking"],
    food: ["Forest produce", "Yam preparations", "Tuber curry", "Wild berry desserts"],
    description: "One of Jharkhand's most unique experiences — stay with the nomadic Birhor community and learn ancient forest living skills.",
    available: true, category: "Primitive Stay"
  }
];

const tribes = [
  {
    name: "Santhal", icon: "🥁", population: "~4M", region: "Eastern Jharkhand",
    color: "#C8843C",
    clothing: "Women wear Panchi-Parhan (sari style). Men wear Dhoti with Gamcha headband.",
    dance: "Dasai, Dong, Baha — performed with synchronized rhythms during harvests and festivals.",
    music: "Banam (string instrument), Tumdak (drum), Tirio (flute) — central to all ceremonies.",
    festivals: "Sohrai (harvest), Baha (flower), Dasain — celebrated with great community fervor.",
    lifestyle: "Settled agriculture, fishing, forest produce. Strong community governance (Village Council).",
    crafts: "Khovar and Sohrai paintings, bamboo furniture, traditional jewelry from beads and shells."
  },
  {
    name: "Munda", icon: "🏹", population: "~2.2M", region: "Central Jharkhand",
    color: "#4A8050",
    clothing: "Women: Kachha style sari in red-white. Men: Lungi or Dhoti with Angavastra.",
    dance: "Jadur, Janthar, Phagua — performed at major cultural events and life-cycle ceremonies.",
    music: "Nagara, Dhol, and Mandar drums create the heartbeat of Munda festivals.",
    festivals: "Sarhul (new year), Karam, Phagu — tied to nature, trees, and seasonal cycles.",
    lifestyle: "Known for Birsa Munda's legacy. Deep connection to forest rights and land stewardship.",
    crafts: "Cane and bamboo weaving, Dhokra metalwork, traditional tattoo art."
  },
  {
    name: "Oraon", icon: "🎵", population: "~2M", region: "Western Jharkhand",
    color: "#C4603A",
    clothing: "Women: Luga (sari) in vibrant hues. Men: Dhoti and shirt for daily wear.",
    dance: "Jadur, Karma, and Jhumar dances — performed with great synchrony and joy.",
    music: "Mandar, Nagara — used in Karma and Sarhul celebrations.",
    festivals: "Karma (worship of Karma tree), Sarhul, and Makar festivals.",
    lifestyle: "Agriculture and forest dwellers, known for strong religious traditions.",
    crafts: "Bamboo baskets, thatch weaving, tribal paintings and wall art."
  },
  {
    name: "Ho", icon: "🌊", population: "~1.4M", region: "Kolhan region",
    color: "#185FA5",
    clothing: "Women: Sari with tribal border patterns. Men: Dhoti and handwoven shawl.",
    dance: "Mage Parab dance — performed during the Maghe harvest festival in January.",
    music: "Tamak (drum) and Turhi (trumpet) — used in community gatherings.",
    festivals: "Maghe, Phagua — vibrant celebrations with community feasting.",
    lifestyle: "Strong warrior heritage. Known for Singhbhum's forest protection movements.",
    crafts: "Iron smelting, traditional weapons crafting, bamboo art."
  },
  {
    name: "Kharia", icon: "🌺", population: "~0.3M", region: "South Jharkhand",
    color: "#7AB87A",
    clothing: "Women: Distinctive handwoven sari with geometric patterns in red and white.",
    dance: "Jhumar and seasonal dances performed at the onset of rain and harvest.",
    music: "Dhole, Mandar — used in communal celebrations.",
    festivals: "Karma, Sarhul, and Nawakhani (new rice) festivals.",
    lifestyle: "Hill dwellers, deep knowledge of medicinal plants and forest ecology.",
    crafts: "Basket weaving, leaf crafts, traditional medicine knowledge."
  },
  {
    name: "Birhor", icon: "🕸️", population: "~10K", region: "Forest regions",
    color: "#6B4423",
    clothing: "Minimal traditional garments made from natural fibers and forest materials.",
    dance: "Ritual dances connected to hunting and forest spirits.",
    music: "Simple percussion instruments and vocal harmonics during ceremonies.",
    festivals: "Seasonal celebrations tied to forest cycles and hunting seasons.",
    lifestyle: "Nomadic rope-makers and hunters. India's most endangered tribal community.",
    crafts: "Rope and net making from Bauhinia creeper — their defining traditional craft."
  }
];

const foods = [
  {
    name: "Dhuska", emoji: "🥘", type: "Snack/Breakfast",
    desc: "Deep-fried rice and dal pancakes — crispy outside, soft inside. The iconic Jharkhand street food.",
    ingredients: ["Rice", "Chana dal", "Onion", "Green chilli", "Turmeric", "Mustard oil"],
    availability: "Most homestays", season: "All year"
  },
  {
    name: "Pitha", emoji: "🍡", type: "Festival Sweet",
    desc: "Steamed or fried rice-flour dumplings stuffed with coconut and jaggery. Made during Sohrai and Karma festivals.",
    ingredients: ["Rice flour", "Coconut", "Jaggery", "Cardamom", "Sesame seeds"],
    availability: "Tribal stays", season: "Festivals"
  },
  {
    name: "Rugra", emoji: "🍄", type: "Wild Delicacy",
    desc: "Wild mushrooms found only in Jharkhand's forests — stir-fried with garlic and forest herbs. A monsoon treasure.",
    ingredients: ["Wild Rugra mushroom", "Garlic", "Onion", "Forest herbs", "Mustard oil"],
    availability: "Monsoon stays", season: "June–September"
  },
  {
    name: "Chilka Roti", emoji: "🫓", type: "Staple Bread",
    desc: "Fermented rice flour flatbread, slightly tangy and nutritious. Eaten with dal or leafy greens.",
    ingredients: ["Rice flour", "Urad dal", "Salt", "Fermented overnight"],
    availability: "All homestays", season: "All year"
  },
  {
    name: "Bamboo Chicken", emoji: "🎋", type: "Signature Dish",
    desc: "Marinated chicken cooked inside fresh bamboo tubes over open fire. The smoke infuses an extraordinary flavor.",
    ingredients: ["Country chicken", "Bamboo tube", "Turmeric", "Ginger-garlic", "Local spices", "Mustard oil"],
    availability: "Netarhat & forest stays", season: "All year"
  },
  {
    name: "Thekua", emoji: "🍪", type: "Festival Sweet",
    desc: "Hard wheat cookies with fennel and coconut, offered to the sun god during Chhath Puja. Sweet and aromatic.",
    ingredients: ["Wheat flour", "Jaggery", "Fennel seeds", "Coconut", "Ghee"],
    availability: "Festival seasons", season: "October–November"
  },
  {
    name: "Handia (Rice Beer)", emoji: "🍺", type: "Traditional Brew",
    desc: "Mildly fermented rice beer made by tribal communities for generations. Used in ceremonies and celebrations.",
    ingredients: ["Rice", "Ranu tablet (herbal starter)", "Water", "10-day fermentation"],
    availability: "Tribal stays only", season: "All year"
  },
  {
    name: "Marka Saag", emoji: "🥬", type: "Forest Green",
    desc: "Wild leafy green cooked with garlic and dried mango. Packed with iron and distinctively earthy in flavor.",
    ingredients: ["Wild Marka leaves", "Garlic", "Dry mango", "Mustard oil", "Panch phoran"],
    availability: "Monsoon stays", season: "July–October"
  }
];

const bookings = [
  { id: "BK2024-001", stay: "Santal Tribal Eco Stay", tourist: "Rahul Sharma", dates: "Dec 15–18", guests: 2, amount: 5100, status: "confirmed" },
  { id: "BK2024-002", stay: "Bamboo Forest Cottage", tourist: "Priya Verma", dates: "Dec 20–22", guests: 3, amount: 6600, status: "pending" },
  { id: "BK2024-003", stay: "Munda Heritage Home", tourist: "Amit Singh", dates: "Jan 5–7", guests: 2, amount: 4200, status: "confirmed" },
  { id: "BK2024-004", stay: "Kharia Village Retreat", tourist: "Sunita Patel", dates: "Jan 10–12", guests: 4, amount: 9600, status: "cancelled" },
];

const adminStats = [
  { label: "Total Homestays", value: "48", icon: "🏡", color: palette.earth3 },
  { label: "Active Providers", value: "36", icon: "👤", color: palette.forest3 },
  { label: "Bookings (Dec)", value: "124", icon: "📅", color: palette.clay },
  { label: "Revenue (₹)", value: "2.4L", icon: "💰", color: palette.earth4 },
];

const StarRating = ({ rating }) => (
  <span style={{ color: "#E8A855", fontSize: 13, letterSpacing: 1 }}>
    {"★".repeat(Math.floor(rating))}{"☆".repeat(5 - Math.floor(rating))}
    <span style={{ color: palette.earth2, marginLeft: 4, fontSize: 12 }}>{rating}</span>
  </span>
);

const Badge = ({ text, color = palette.earth3 }) => (
  <span style={{
    background: color + "22", color, border: `1px solid ${color}44`,
    borderRadius: 20, padding: "2px 10px", fontSize: 11, fontWeight: 600, whiteSpace: "nowrap"
  }}>{text}</span>
);

const TribalPattern = ({ style }) => (
  <div style={{ position: "absolute", inset: 0, ...style, pointerEvents: "none", overflow: "hidden" }}>
    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="tp" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
          <circle cx="20" cy="20" r="1.5" fill="currentColor" opacity="0.15"/>
          <line x1="0" y1="0" x2="20" y2="20" stroke="currentColor" strokeWidth="0.4" opacity="0.1"/>
          <line x1="40" y1="0" x2="20" y2="20" stroke="currentColor" strokeWidth="0.4" opacity="0.1"/>
          <polygon points="20,8 24,16 16,16" fill="none" stroke="currentColor" strokeWidth="0.5" opacity="0.1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#tp)"/>
    </svg>
  </div>
);

export default function JharkhandDashboard() {
  const [activeTab, setActiveTab] = useState("homestays");
  const [selectedTribe, setSelectedTribe] = useState(null);
  const [selectedFood, setSelectedFood] = useState(null);
  const [bookingModal, setBookingModal] = useState(null);
  const [adminView, setAdminView] = useState("overview");
  const [filterTribe, setFilterTribe] = useState("All");
  const [bookingForm, setBookingForm] = useState({ checkin: "", checkout: "", guests: 1, food: "basic" });
  const [booked, setBooked] = useState(false);
  const [providerForm, setProviderForm] = useState({ name: "", village: "", district: "", tribe: "", price: "", desc: "" });
  const [providerSubmitted, setProviderSubmitted] = useState(false);
  const [searchQ, setSearchQ] = useState("");

  const tabs = [
    { id: "homestays", label: "🏡 Homestays" },
    { id: "culture", label: "🎭 Tribal Culture" },
    { id: "food", label: "🍽️ Traditional Food" },
    { id: "booking", label: "📅 My Bookings" },
    { id: "provider", label: "🌿 List Your Stay" },
    { id: "admin", label: "⚙️ Admin Panel" },
  ];

  const filteredHomestays = homestays.filter(h =>
    (filterTribe === "All" || h.tribe === filterTribe) &&
    (h.name.toLowerCase().includes(searchQ.toLowerCase()) || h.village.toLowerCase().includes(searchQ.toLowerCase()))
  );

  return (
    <div style={{ fontFamily: "'Georgia', serif", background: palette.cream, minHeight: "100vh", color: palette.earth1 }}>
      {/* HEADER */}
      <div style={{ background: palette.forest1, color: "#FAF3E6", padding: "0", position: "relative", overflow: "hidden" }}>
        <TribalPattern style={{ color: "#FAF3E6" }} />
        <div style={{ padding: "24px 28px 20px", position: "relative", zIndex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 8 }}>
            <div style={{ width: 52, height: 52, borderRadius: "50%", background: palette.earth3, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 26, border: `3px solid ${palette.earth4}` }}>🌿</div>
            <div>
              <div style={{ fontSize: 22, fontWeight: 700, letterSpacing: 1 }}>झारखंड आतिथ्य</div>
              <div style={{ fontSize: 13, color: palette.sand2, letterSpacing: 2 }}>JHARKHAND LOCAL CULTURE & HOMESTAY</div>
            </div>
            <div style={{ marginLeft: "auto", textAlign: "right" }}>
              <div style={{ fontSize: 11, color: palette.sand3 }}>Eco · Tribal · Authentic</div>
              <div style={{ fontSize: 11, color: palette.forest4, marginTop: 2 }}>🌱 Sustainable Tourism Initiative</div>
            </div>
          </div>
          {/* Decorative border */}
          <div style={{ height: 3, background: `linear-gradient(90deg, ${palette.earth4}, ${palette.forest3}, ${palette.earth4})`, borderRadius: 2, marginTop: 8 }} />
        </div>
        {/* NAV */}
        <div style={{ display: "flex", overflowX: "auto", padding: "0 28px", gap: 2, position: "relative", zIndex: 1 }}>
          {tabs.map(t => (
            <button key={t.id} onClick={() => setActiveTab(t.id)} style={{
              background: activeTab === t.id ? palette.earth3 : "transparent",
              color: activeTab === t.id ? "#fff" : palette.sand2,
              border: "none", padding: "10px 16px", cursor: "pointer",
              borderRadius: "8px 8px 0 0", fontSize: 13, fontWeight: activeTab === t.id ? 600 : 400,
              whiteSpace: "nowrap", transition: "all 0.2s"
            }}>{t.label}</button>
          ))}
        </div>
      </div>

      <div style={{ padding: "24px 28px" }}>

        {/* ======================== HOMESTAYS TAB ======================== */}
        {activeTab === "homestays" && (
          <div>
            <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap", alignItems: "center" }}>
              <input
                value={searchQ} onChange={e => setSearchQ(e.target.value)}
                placeholder="🔍 Search homestay or village..."
                style={{ flex: 1, minWidth: 200, padding: "10px 14px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, background: "#fff", fontSize: 14, fontFamily: "Georgia, serif" }}
              />
              <select value={filterTribe} onChange={e => setFilterTribe(e.target.value)}
                style={{ padding: "10px 14px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, background: "#fff", fontSize: 13, cursor: "pointer" }}>
                <option value="All">All Tribes</option>
                {["Santhal","Munda","Oraon","Ho","Kharia","Birhor"].map(t => <option key={t}>{t}</option>)}
              </select>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 18 }}>
              {filteredHomestays.map(h => (
                <div key={h.id} style={{
                  background: "#fff", borderRadius: 14, overflow: "hidden",
                  border: `1.5px solid ${palette.sand2}`, boxShadow: "0 2px 12px rgba(59,42,26,0.08)",
                  transition: "transform 0.2s", cursor: "pointer",
                  opacity: h.available ? 1 : 0.7
                }}
                  onMouseEnter={e => e.currentTarget.style.transform = "translateY(-3px)"}
                  onMouseLeave={e => e.currentTarget.style.transform = "translateY(0)"}
                >
                  {/* Image placeholder */}
                  <div style={{ height: 140, background: `linear-gradient(135deg, ${palette.forest2}, ${palette.earth3})`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 60, position: "relative" }}>
                    <TribalPattern style={{ color: "#FAF3E6" }} />
                    <span style={{ position: "relative", zIndex: 1 }}>{h.image}</span>
                    <div style={{ position: "absolute", top: 10, right: 10, background: h.available ? palette.forest3 : "#888", color: "#fff", borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 600 }}>
                      {h.available ? "✓ Available" : "Booked"}
                    </div>
                    <div style={{ position: "absolute", top: 10, left: 10 }}>
                      <Badge text={h.category} color={palette.earth3} />
                    </div>
                  </div>
                  <div style={{ padding: "16px 16px 14px" }}>
                    <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 4 }}>{h.name}</div>
                    <div style={{ fontSize: 12, color: palette.earth3, marginBottom: 6 }}>👨‍👩‍👧 {h.owner} · 📍 {h.village}, {h.district}</div>
                    <div style={{ marginBottom: 8 }}><StarRating rating={h.rating} /> <span style={{ fontSize: 11, color: "#999" }}>({h.reviews} reviews)</span></div>
                    <div style={{ fontSize: 12, color: "#555", marginBottom: 10, lineHeight: 1.5 }}>{h.description.slice(0, 100)}...</div>

                    <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginBottom: 10 }}>
                      {h.facilities.slice(0, 3).map(f => (
                        <span key={f} style={{ background: palette.forest1 + "15", color: palette.forest2, borderRadius: 20, padding: "2px 8px", fontSize: 10 }}>✓ {f}</span>
                      ))}
                    </div>

                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 10, paddingTop: 10, borderTop: `1px solid ${palette.sand2}` }}>
                      <div>
                        <span style={{ fontSize: 20, fontWeight: 700, color: palette.earth2 }}>₹{h.price}</span>
                        <span style={{ fontSize: 12, color: "#999" }}>/night</span>
                      </div>
                      <button
                        onClick={() => { if (h.available) { setBookingModal(h); setBooked(false); setBookingForm({ checkin: "", checkout: "", guests: 1, food: "basic" }); } }}
                        style={{
                          background: h.available ? palette.earth3 : "#ccc",
                          color: "#fff", border: "none", borderRadius: 8,
                          padding: "8px 18px", cursor: h.available ? "pointer" : "not-allowed",
                          fontSize: 13, fontWeight: 600
                        }}
                      >
                        {h.available ? "Book Now →" : "Unavailable"}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ======================== CULTURE TAB ======================== */}
        {activeTab === "culture" && (
          <div>
            <div style={{ marginBottom: 20 }}>
              <h2 style={{ color: palette.earth1, fontSize: 22, margin: "0 0 6px" }}>Tribal Communities of Jharkhand</h2>
              <p style={{ color: palette.earth3, fontSize: 14, margin: 0 }}>Jharkhand is home to 32 tribal communities. Explore the six major ones below.</p>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 14 }}>
              {tribes.map(tribe => (
                <div key={tribe.name}
                  onClick={() => setSelectedTribe(selectedTribe?.name === tribe.name ? null : tribe)}
                  style={{
                    background: "#fff", borderRadius: 12, padding: 18, cursor: "pointer",
                    border: `2px solid ${selectedTribe?.name === tribe.name ? tribe.color : palette.sand2}`,
                    transition: "all 0.2s", boxShadow: selectedTribe?.name === tribe.name ? `0 4px 20px ${tribe.color}33` : "0 2px 8px rgba(0,0,0,0.05)"
                  }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 10 }}>
                    <div style={{ width: 48, height: 48, borderRadius: "50%", background: tribe.color + "20", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24, border: `2px solid ${tribe.color}` }}>
                      {tribe.icon}
                    </div>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: 16 }}>{tribe.name}</div>
                      <div style={{ fontSize: 11, color: "#888" }}>Pop: {tribe.population} · {tribe.region}</div>
                    </div>
                  </div>

                  {selectedTribe?.name === tribe.name && (
                    <div style={{ marginTop: 14, borderTop: `1.5px solid ${tribe.color}33`, paddingTop: 14 }}>
                      {[
                        { label: "👗 Clothing", val: tribe.clothing },
                        { label: "💃 Dance", val: tribe.dance },
                        { label: "🎵 Music", val: tribe.music },
                        { label: "🎉 Festivals", val: tribe.festivals },
                        { label: "🌿 Lifestyle", val: tribe.lifestyle },
                        { label: "🧶 Crafts", val: tribe.crafts },
                      ].map(item => (
                        <div key={item.label} style={{ marginBottom: 10 }}>
                          <div style={{ fontSize: 12, fontWeight: 600, color: tribe.color, marginBottom: 2 }}>{item.label}</div>
                          <div style={{ fontSize: 13, color: "#444", lineHeight: 1.5 }}>{item.val}</div>
                        </div>
                      ))}
                    </div>
                  )}

                  {selectedTribe?.name !== tribe.name && (
                    <div style={{ fontSize: 12, color: "#999", textAlign: "center", marginTop: 4 }}>Click to explore →</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ======================== FOOD TAB ======================== */}
        {activeTab === "food" && (
          <div>
            <div style={{ marginBottom: 20 }}>
              <h2 style={{ color: palette.earth1, fontSize: 22, margin: "0 0 6px" }}>Traditional Flavours of Jharkhand</h2>
              <p style={{ color: palette.earth3, fontSize: 14 }}>Taste the forest, the festivals, and the heritage in every bite.</p>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 16 }}>
              {foods.map(food => (
                <div key={food.name}
                  onClick={() => setSelectedFood(selectedFood?.name === food.name ? null : food)}
                  style={{
                    background: "#fff", borderRadius: 14, overflow: "hidden", cursor: "pointer",
                    border: `1.5px solid ${selectedFood?.name === food.name ? palette.earth4 : palette.sand2}`,
                    transition: "all 0.2s", boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
                  }}>
                  <div style={{ height: 90, background: `linear-gradient(135deg, ${palette.earth4}33, ${palette.sand2})`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 48, position: "relative" }}>
                    <TribalPattern style={{ color: palette.earth3 }} />
                    <span style={{ position: "relative", zIndex: 1 }}>{food.emoji}</span>
                    <div style={{ position: "absolute", top: 8, right: 8 }}>
                      <Badge text={food.type} color={palette.earth3} />
                    </div>
                  </div>
                  <div style={{ padding: "14px 16px" }}>
                    <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 4 }}>{food.name}</div>
                    <div style={{ fontSize: 12, color: "#555", lineHeight: 1.5, marginBottom: 8 }}>{food.desc}</div>

                    {selectedFood?.name === food.name && (
                      <div style={{ borderTop: `1px dashed ${palette.sand3}`, paddingTop: 10, marginTop: 6 }}>
                        <div style={{ fontSize: 12, fontWeight: 600, color: palette.earth3, marginBottom: 6 }}>🧄 Ingredients</div>
                        <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                          {food.ingredients.map(ing => (
                            <span key={ing} style={{ background: palette.sand1, color: palette.earth2, borderRadius: 20, padding: "2px 8px", fontSize: 11 }}>{ing}</span>
                          ))}
                        </div>
                        <div style={{ marginTop: 10, fontSize: 12 }}>
                          <span style={{ color: palette.forest3, fontWeight: 600 }}>📍 Available: </span>
                          <span style={{ color: "#555" }}>{food.availability}</span>
                        </div>
                        <div style={{ fontSize: 12 }}>
                          <span style={{ color: palette.forest3, fontWeight: 600 }}>🗓 Season: </span>
                          <span style={{ color: "#555" }}>{food.season}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ======================== BOOKING HISTORY TAB ======================== */}
        {activeTab === "booking" && (
          <div>
            <h2 style={{ color: palette.earth1, fontSize: 22, marginBottom: 6 }}>My Booking History</h2>
            <p style={{ color: palette.earth3, fontSize: 14, marginBottom: 20 }}>Your recent and upcoming homestay reservations.</p>

            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {bookings.map(b => (
                <div key={b.id} style={{
                  background: "#fff", borderRadius: 12, padding: "16px 20px",
                  border: `1.5px solid ${b.status === "confirmed" ? palette.forest3 + "66" : b.status === "cancelled" ? "#f0000044" : palette.earth4 + "66"}`,
                  display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12
                }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 15 }}>{b.stay}</div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 2 }}>ID: {b.id} · Tourist: {b.tourist}</div>
                    <div style={{ fontSize: 12, color: palette.earth3, marginTop: 2 }}>📅 {b.dates} · 👥 {b.guests} guests</div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 18, fontWeight: 700, color: palette.earth2 }}>₹{b.amount.toLocaleString()}</div>
                    <span style={{
                      display: "inline-block", marginTop: 6,
                      background: b.status === "confirmed" ? palette.forest3 + "22" : b.status === "cancelled" ? "#f0000022" : palette.earth4 + "22",
                      color: b.status === "confirmed" ? palette.forest2 : b.status === "cancelled" ? "#c00" : palette.earth3,
                      borderRadius: 20, padding: "3px 12px", fontSize: 12, fontWeight: 600
                    }}>
                      {b.status === "confirmed" ? "✓ Confirmed" : b.status === "cancelled" ? "✕ Cancelled" : "⏳ Pending"}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div style={{ marginTop: 24, background: palette.sand1, borderRadius: 12, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 32, marginBottom: 8 }}>🌿</div>
              <div style={{ fontWeight: 600, color: palette.earth2 }}>Your stays support local communities directly</div>
              <div style={{ fontSize: 13, color: "#777", marginTop: 4 }}>100% of your booking amount goes to local village families and cooperatives</div>
            </div>
          </div>
        )}

        {/* ======================== PROVIDER TAB ======================== */}
        {activeTab === "provider" && (
          <div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
              <div>
                <h2 style={{ color: palette.earth1, fontSize: 22, marginBottom: 6 }}>Register Your Homestay</h2>
                <p style={{ color: palette.earth3, fontSize: 14, marginBottom: 20 }}>Join our network and welcome tourists to your home and village.</p>

                {providerSubmitted ? (
                  <div style={{ background: palette.forest1 + "15", border: `2px solid ${palette.forest3}`, borderRadius: 14, padding: 32, textAlign: "center" }}>
                    <div style={{ fontSize: 48, marginBottom: 12 }}>🎉</div>
                    <div style={{ fontWeight: 700, fontSize: 18, color: palette.forest2, marginBottom: 6 }}>Application Submitted!</div>
                    <div style={{ fontSize: 14, color: "#555" }}>Our team will verify your details and contact you within 3 working days.</div>
                    <button onClick={() => setProviderSubmitted(false)} style={{ marginTop: 16, background: palette.forest2, color: "#fff", border: "none", borderRadius: 8, padding: "10px 24px", cursor: "pointer", fontSize: 14 }}>Submit Another</button>
                  </div>
                ) : (
                  <div style={{ background: "#fff", borderRadius: 14, padding: 24, border: `1.5px solid ${palette.sand2}` }}>
                    {[
                      { label: "Your / Family Name", field: "name", placeholder: "e.g. Birsa Munda" },
                      { label: "Village Name", field: "village", placeholder: "e.g. Deoghar Village" },
                      { label: "District", field: "district", placeholder: "e.g. Deoghar" },
                      { label: "Price per Night (₹)", field: "price", placeholder: "e.g. 800" },
                    ].map(item => (
                      <div key={item.field} style={{ marginBottom: 14 }}>
                        <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 4 }}>{item.label}</label>
                        <input
                          value={providerForm[item.field]} onChange={e => setProviderForm(f => ({ ...f, [item.field]: e.target.value }))}
                          placeholder={item.placeholder}
                          style={{ width: "100%", padding: "10px 12px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, fontSize: 14, boxSizing: "border-box", fontFamily: "Georgia, serif" }}
                        />
                      </div>
                    ))}
                    <div style={{ marginBottom: 14 }}>
                      <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 4 }}>Tribal Community</label>
                      <select value={providerForm.tribe} onChange={e => setProviderForm(f => ({ ...f, tribe: e.target.value }))}
                        style={{ width: "100%", padding: "10px 12px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, fontSize: 14, background: "#fff" }}>
                        <option value="">Select Community</option>
                        {["Santhal","Munda","Oraon","Ho","Kharia","Birhor","Other"].map(t => <option key={t}>{t}</option>)}
                      </select>
                    </div>
                    <div style={{ marginBottom: 18 }}>
                      <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 4 }}>Describe Your Homestay</label>
                      <textarea value={providerForm.desc} onChange={e => setProviderForm(f => ({ ...f, desc: e.target.value }))}
                        placeholder="Tell tourists what makes your home special..."
                        rows={3}
                        style={{ width: "100%", padding: "10px 12px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, fontSize: 14, boxSizing: "border-box", fontFamily: "Georgia, serif", resize: "vertical" }} />
                    </div>
                    <button
                      onClick={() => { if (providerForm.name && providerForm.village) setProviderSubmitted(true); }}
                      style={{ width: "100%", background: palette.earth3, color: "#fff", border: "none", borderRadius: 10, padding: "12px", fontSize: 15, fontWeight: 700, cursor: "pointer" }}>
                      🌿 Submit for Approval
                    </button>
                  </div>
                )}
              </div>

              <div>
                <h3 style={{ color: palette.earth1, fontSize: 18, marginBottom: 14 }}>Why List with Us?</h3>
                {[
                  { icon: "💰", title: "Direct Income", desc: "Earn ₹15,000–40,000/month from tourist stays without any middleman." },
                  { icon: "🌍", title: "Global Visibility", desc: "Your home reaches tourists from across India and the world." },
                  { icon: "🤝", title: "Community Support", desc: "We train and support you with photography, pricing, and guest management." },
                  { icon: "📱", title: "Easy Management", desc: "Simple app to manage bookings, dates, and payments on your phone." },
                  { icon: "🏅", title: "Certification", desc: "Get certified as an Eco Tourism Provider by Jharkhand Tourism Board." },
                ].map(item => (
                  <div key={item.title} style={{ display: "flex", gap: 14, marginBottom: 16, background: "#fff", borderRadius: 10, padding: "14px 16px", border: `1px solid ${palette.sand2}` }}>
                    <span style={{ fontSize: 24 }}>{item.icon}</span>
                    <div>
                      <div style={{ fontWeight: 700, color: palette.earth2, fontSize: 14 }}>{item.title}</div>
                      <div style={{ fontSize: 13, color: "#666", lineHeight: 1.5 }}>{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ======================== ADMIN TAB ======================== */}
        {activeTab === "admin" && (
          <div>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
              <h2 style={{ color: palette.earth1, fontSize: 22, margin: 0 }}>Admin Dashboard</h2>
              <div style={{ display: "flex", gap: 8 }}>
                {["overview", "bookings", "providers"].map(v => (
                  <button key={v} onClick={() => setAdminView(v)} style={{
                    background: adminView === v ? palette.earth3 : "#fff",
                    color: adminView === v ? "#fff" : palette.earth2,
                    border: `1.5px solid ${adminView === v ? palette.earth3 : palette.sand3}`,
                    borderRadius: 8, padding: "7px 16px", cursor: "pointer", fontSize: 13, fontWeight: 600, textTransform: "capitalize"
                  }}>{v}</button>
                ))}
              </div>
            </div>

            {adminView === "overview" && (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 14, marginBottom: 24 }}>
                  {adminStats.map(s => (
                    <div key={s.label} style={{ background: "#fff", borderRadius: 12, padding: 18, border: `1.5px solid ${palette.sand2}`, textAlign: "center" }}>
                      <div style={{ fontSize: 28, marginBottom: 6 }}>{s.icon}</div>
                      <div style={{ fontSize: 24, fontWeight: 700, color: s.color }}>{s.value}</div>
                      <div style={{ fontSize: 12, color: "#888", marginTop: 2 }}>{s.label}</div>
                    </div>
                  ))}
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
                  <div style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1.5px solid ${palette.sand2}` }}>
                    <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 14, color: palette.earth2 }}>📋 Pending Approvals</div>
                    {[
                      { name: "Hemant Soren", type: "Homestay", district: "Ranchi", time: "2h ago" },
                      { name: "Sunita Hembrom", type: "Food Provider", district: "Dumka", time: "5h ago" },
                      { name: "Raju Munda", type: "Homestay", district: "Khunti", time: "1d ago" },
                    ].map(p => (
                      <div key={p.name} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 0", borderBottom: `1px dashed ${palette.sand2}` }}>
                        <div>
                          <div style={{ fontWeight: 600, fontSize: 13 }}>{p.name}</div>
                          <div style={{ fontSize: 11, color: "#999" }}>{p.type} · {p.district} · {p.time}</div>
                        </div>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button style={{ background: palette.forest3 + "22", color: palette.forest2, border: `1px solid ${palette.forest3}`, borderRadius: 6, padding: "4px 10px", cursor: "pointer", fontSize: 12 }}>✓ Approve</button>
                          <button style={{ background: "#fee", color: "#c00", border: "1px solid #fcc", borderRadius: 6, padding: "4px 10px", cursor: "pointer", fontSize: 12 }}>✕ Reject</button>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1.5px solid ${palette.sand2}` }}>
                    <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 14, color: palette.earth2 }}>📊 Monthly Stats</div>
                    {[
                      { label: "New Registrations", value: 14, max: 20, color: palette.earth3 },
                      { label: "Verified Providers", value: 8, max: 14, color: palette.forest3 },
                      { label: "Tourist Arrivals", value: 87, max: 120, color: palette.clay },
                      { label: "Revenue (₹L)", value: 2.4, max: 5, color: palette.earth4 },
                    ].map(s => (
                      <div key={s.label} style={{ marginBottom: 14 }}>
                        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 5 }}>
                          <span style={{ color: palette.earth1 }}>{s.label}</span>
                          <span style={{ fontWeight: 700, color: s.color }}>{s.value}</span>
                        </div>
                        <div style={{ height: 6, background: palette.sand2, borderRadius: 3 }}>
                          <div style={{ height: 6, background: s.color, borderRadius: 3, width: `${(s.value / s.max) * 100}%`, transition: "width 0.5s" }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {adminView === "bookings" && (
              <div style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1.5px solid ${palette.sand2}` }}>
                <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 14, color: palette.earth2 }}>All Bookings</div>
                {bookings.map(b => (
                  <div key={b.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: `1px dashed ${palette.sand2}`, flexWrap: "wrap", gap: 8 }}>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 14 }}>{b.stay}</div>
                      <div style={{ fontSize: 12, color: "#888" }}>{b.tourist} · {b.dates} · {b.guests} guests</div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                      <span style={{ fontWeight: 700, color: palette.earth2 }}>₹{b.amount.toLocaleString()}</span>
                      <span style={{
                        background: b.status === "confirmed" ? "#e8f5e9" : b.status === "cancelled" ? "#ffebee" : "#fff8e1",
                        color: b.status === "confirmed" ? "#2e7d32" : b.status === "cancelled" ? "#c62828" : "#f57f17",
                        borderRadius: 20, padding: "3px 12px", fontSize: 12, fontWeight: 600
                      }}>{b.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {adminView === "providers" && (
              <div style={{ background: "#fff", borderRadius: 12, padding: 20, border: `1.5px solid ${palette.sand2}` }}>
                <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 14, color: palette.earth2 }}>Registered Providers</div>
                {homestays.map(h => (
                  <div key={h.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: `1px dashed ${palette.sand2}`, flexWrap: "wrap", gap: 8 }}>
                    <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                      <span style={{ fontSize: 24 }}>{h.image}</span>
                      <div>
                        <div style={{ fontWeight: 600, fontSize: 14 }}>{h.owner}</div>
                        <div style={{ fontSize: 12, color: "#888" }}>{h.name} · {h.district}</div>
                        <Badge text={h.tribe} color={palette.earth3} />
                      </div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <span style={{ fontSize: 13, color: palette.forest3 }}>✓ Verified</span>
                      <button style={{ background: palette.earth3, color: "#fff", border: "none", borderRadius: 6, padding: "5px 12px", cursor: "pointer", fontSize: 12 }}>View Profile</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </div>

      {/* ======================== BOOKING MODAL ======================== */}
      {bookingModal && (
        <div style={{
          position: "fixed", inset: 0, background: "rgba(20,10,5,0.7)", zIndex: 100,
          display: "flex", alignItems: "center", justifyContent: "center", padding: 20
        }} onClick={() => setBookingModal(null)}>
          <div onClick={e => e.stopPropagation()} style={{
            background: palette.cream, borderRadius: 18, maxWidth: 480, width: "100%",
            maxHeight: "90vh", overflow: "auto", border: `2px solid ${palette.earth4}`
          }}>
            {/* Modal header */}
            <div style={{ background: palette.forest1, color: "#FAF3E6", padding: "20px 24px", borderRadius: "16px 16px 0 0", position: "relative" }}>
              <TribalPattern style={{ color: "#FAF3E6" }} />
              <div style={{ position: "relative", zIndex: 1 }}>
                <div style={{ fontSize: 32, marginBottom: 4 }}>{bookingModal.image}</div>
                <div style={{ fontWeight: 700, fontSize: 18 }}>{bookingModal.name}</div>
                <div style={{ fontSize: 13, color: palette.sand2 }}>📍 {bookingModal.village}, {bookingModal.district}</div>
              </div>
              <button onClick={() => setBookingModal(null)} style={{
                position: "absolute", top: 16, right: 16, background: "rgba(255,255,255,0.2)",
                border: "none", color: "#fff", borderRadius: "50%", width: 28, height: 28, cursor: "pointer", fontSize: 16
              }}>✕</button>
            </div>

            <div style={{ padding: "24px" }}>
              {booked ? (
                <div style={{ textAlign: "center", padding: "20px 0" }}>
                  <div style={{ fontSize: 56, marginBottom: 12 }}>🎉</div>
                  <div style={{ fontWeight: 700, fontSize: 20, color: palette.forest2, marginBottom: 8 }}>Booking Confirmed!</div>
                  <div style={{ fontSize: 14, color: "#555", lineHeight: 1.6 }}>
                    Thank you for booking with <strong>{bookingModal.owner}</strong>!<br />
                    You'll receive confirmation details shortly.<br />
                    Your stay supports the local {bookingModal.tribe} community. 🌿
                  </div>
                  <button onClick={() => setBookingModal(null)} style={{
                    marginTop: 20, background: palette.earth3, color: "#fff", border: "none",
                    borderRadius: 10, padding: "12px 28px", cursor: "pointer", fontSize: 15, fontWeight: 700
                  }}>Close</button>
                </div>
              ) : (
                <>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 16 }}>
                    <div>
                      <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 4 }}>Check-in Date</label>
                      <input type="date" value={bookingForm.checkin} onChange={e => setBookingForm(f => ({ ...f, checkin: e.target.value }))}
                        style={{ width: "100%", padding: "10px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, fontSize: 14, boxSizing: "border-box" }} />
                    </div>
                    <div>
                      <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 4 }}>Check-out Date</label>
                      <input type="date" value={bookingForm.checkout} onChange={e => setBookingForm(f => ({ ...f, checkout: e.target.value }))}
                        style={{ width: "100%", padding: "10px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, fontSize: 14, boxSizing: "border-box" }} />
                    </div>
                  </div>

                  <div style={{ marginBottom: 16 }}>
                    <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 4 }}>Number of Guests</label>
                    <input type="number" min={1} max={8} value={bookingForm.guests} onChange={e => setBookingForm(f => ({ ...f, guests: Number(e.target.value) }))}
                      style={{ width: "100%", padding: "10px", borderRadius: 8, border: `1.5px solid ${palette.sand3}`, fontSize: 14, boxSizing: "border-box" }} />
                  </div>

                  <div style={{ marginBottom: 20 }}>
                    <label style={{ fontSize: 13, fontWeight: 600, color: palette.earth2, display: "block", marginBottom: 8 }}>Food Package</label>
                    {[
                      { val: "basic", label: "Basic (Breakfast only)", extra: 0 },
                      { val: "standard", label: "Standard (2 meals)", extra: 150 },
                      { val: "full", label: "Full Board (3 meals + cultural snacks)", extra: 300 },
                    ].map(pkg => (
                      <label key={pkg.val} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", borderRadius: 8, marginBottom: 8, cursor: "pointer", background: bookingForm.food === pkg.val ? palette.earth3 + "15" : "#fff", border: `1.5px solid ${bookingForm.food === pkg.val ? palette.earth3 : palette.sand2}` }}>
                        <input type="radio" name="food" value={pkg.val} checked={bookingForm.food === pkg.val} onChange={() => setBookingForm(f => ({ ...f, food: pkg.val }))} />
                        <span style={{ fontSize: 13 }}>{pkg.label}</span>
                        {pkg.extra > 0 && <span style={{ marginLeft: "auto", color: palette.earth3, fontWeight: 600, fontSize: 13 }}>+₹{pkg.extra}/night</span>}
                      </label>
                    ))}
                  </div>

                  <div style={{ background: palette.sand1, borderRadius: 10, padding: "14px 16px", marginBottom: 20 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
                      <span>Stay ({bookingModal.price}/night × {bookingForm.guests} guest{bookingForm.guests > 1 ? "s" : ""})</span>
                      <span>₹{bookingModal.price * bookingForm.guests}</span>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
                      <span>Food package</span>
                      <span>₹{bookingForm.food === "basic" ? 0 : bookingForm.food === "standard" ? 150 : 300}/night</span>
                    </div>
                    <div style={{ borderTop: `1px dashed ${palette.sand3}`, paddingTop: 8, marginTop: 4, display: "flex", justifyContent: "space-between", fontWeight: 700, fontSize: 15 }}>
                      <span>Per night total</span>
                      <span style={{ color: palette.earth2 }}>₹{bookingModal.price * bookingForm.guests + (bookingForm.food === "basic" ? 0 : bookingForm.food === "standard" ? 150 : 300)}</span>
                    </div>
                  </div>

                  <div style={{ display: "flex", gap: 10 }}>
                    <button onClick={() => setBookingModal(null)} style={{ flex: 1, background: "#fff", color: palette.earth2, border: `1.5px solid ${palette.sand3}`, borderRadius: 10, padding: "12px", cursor: "pointer", fontSize: 14 }}>Cancel</button>
                    <button onClick={() => setBooked(true)} style={{ flex: 2, background: palette.earth3, color: "#fff", border: "none", borderRadius: 10, padding: "12px", cursor: "pointer", fontSize: 15, fontWeight: 700 }}>
                      🌿 Confirm Booking
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* FOOTER */}
      <div style={{ background: palette.earth1, color: palette.sand2, padding: "20px 28px", marginTop: 32, textAlign: "center" }}>
        <div style={{ fontSize: 20, marginBottom: 6 }}>🌿 झारखंड पर्यटन · Jharkhand Tourism</div>
        <div style={{ fontSize: 12, color: palette.sand3 }}>Eco & Cultural Tourism Platform · Supporting 32 Tribal Communities · Sustainable · Inclusive · Authentic</div>
        <div style={{ fontSize: 11, color: palette.earth4, marginTop: 6 }}>Government of Jharkhand Initiative · All bookings directly benefit local village families</div>
      </div>
    </div>
  );
}
