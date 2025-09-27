// Dummy Vendors (later connect to Flask API)
const dummyVendors = [
  { id: 1, name: "Aayush Tailor", business_name: "Elegant Stitches", category: "Tailor", city: "Jaipur", description: "Custom clothing and modern designs.", phone: "9998887777" },
  { id: 2, name: "Rohan Jewels", business_name: "Rohan Goldsmith", category: "Jewellery", city: "Jaipur", description: "Traditional and modern gold jewellery.", whatsapp: "9995554444" }
];

// Create vendor card
function makeCard(v){
  const name = v.business_name ? v.business_name : (v.name || "Unnamed Vendor");
  const category = v.category || "Uncategorized";
  const city = v.city || "Jaipur";
  const desc = v.description ? v.description.slice(0, 90) : "No description available";

  return `
    <div data-aos="fade-up" data-aos-delay="${v.id * 100}"
         class="bg-white/30 backdrop-blur-md rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition duration-300">
      <img src="placeholder.jpg" class="w-full h-48 object-cover" alt="${name}" />
      <div class="p-5 text-gray-900">
        <h3 class="text-lg font-bold text-gray-800">${name}</h3>
        <p class="text-sm text-gray-600 mb-2">${category} • ${city}</p>
        <p class="text-sm text-gray-700 mb-3">${desc}...</p>
        <div class="flex justify-between items-center">
          <a href="vendor.html?id=${v.id}" 
             class="text-sm font-semibold text-indigo-600 hover:text-indigo-800">
             View Profile →
          </a>
          <div class="flex gap-2">
            ${v.phone ? `<a href="tel:${v.phone}" class="text-xs px-3 py-1 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition">Call</a>` : ''}
            ${v.whatsapp ? `<a href="https://wa.me/${v.whatsapp}" target="_blank" class="text-xs px-3 py-1 bg-green-600 text-white rounded-full hover:bg-green-700 transition">WhatsApp</a>` : ''}
          </div>
        </div>
      </div>
    </div>
  `;
}

// Render vendors
function render(){
  const grid = document.getElementById('vendorsGrid');
  if(!grid) return; // safety check

  const search = document.getElementById('searchInput')?.value.toLowerCase() || "";
  const filtered = dummyVendors.filter(v=>{
    const text = `${v.business_name} ${v.name} ${v.category} ${v.city}`.toLowerCase();
    return (!search || text.includes(search));
  });

  grid.innerHTML = filtered.map(makeCard).join('');
  document.getElementById('noResults').classList.toggle('hidden', filtered.length>0);
  AOS.refresh();
}

// Events
document.addEventListener('DOMContentLoaded', ()=>{
  render();

  const searchBtn = document.getElementById('searchBtn');
  const searchInput = document.getElementById('searchInput');

  if(searchBtn) searchBtn.onclick = render;
  if(searchInput) searchInput.onkeyup = (e)=>{ if(e.key==='Enter') render(); };

  // Optional CTA Register button
  const openRegister = document.getElementById('openRegister');
  if(openRegister){
    openRegister.onclick = ()=> alert("Registration form coming soon!");
  }
});

// Navbar Mobile Menu
document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById("menuBtn");
  const closeMenu = document.getElementById("closeMenu");
  const mobileMenu = document.getElementById("mobileMenu");

  if(menuBtn && closeMenu && mobileMenu){
    menuBtn.addEventListener("click", () => {
      mobileMenu.classList.remove("hidden");
    });
    closeMenu.addEventListener("click", () => {
      mobileMenu.classList.add("hidden");
    });
  }

  // Mobile Register button
  const mobileRegister = document.getElementById("mobileRegister");
  if(mobileRegister){
    mobileRegister.addEventListener("click", () => {
      alert("Registration form coming soon!");
      mobileMenu.classList.add("hidden");
    });
  }
});
