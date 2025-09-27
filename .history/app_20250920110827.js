// Dummy data (later connect with Flask)
const dummyVendors = [
  { id: 1, name: "Aayush Tailor", business_name: "Elegant Stitches", category: "Tailor", city: "Jaipur", description: "Custom clothing and modern designs.", phone: "9998887777" },
  { id: 2, name: "Rohan Jewels", business_name: "Rohan Goldsmith", category: "Jewellery", city: "Jaipur", description: "Traditional and modern gold jewellery.", whatsapp: "9995554444" }
];

function makeCard(v){
  return `
    <div data-aos="fade-up" class="bg-white rounded-lg shadow overflow-hidden">
      <img src="placeholder.jpg" class="w-full h-44 object-cover" />
      <div class="p-4">
        <h3 class="text-lg font-semibold">${v.business_name || v.name}</h3>
        <p class="text-sm text-gray-500">${v.category} • ${v.city}</p>
        <p class="mt-2 text-sm text-gray-700">${(v.description||'').slice(0,120)}</p>
        <div class="mt-3 flex justify-between items-center">
          <a href="vendor.html?id=${v.id}" class="text-sm text-indigo-600">View profile</a>
          <div class="flex gap-2">
            ${v.phone?`<a href="tel:${v.phone}" class="text-sm px-3 py-1 border rounded">Call</a>`:''}
            ${v.whatsapp?`<a href="https://wa.me/${v.whatsapp}" target="_blank" class="text-sm px-3 py-1 border rounded">WhatsApp</a>`:''}
          </div>
        </div>
      </div>
    </div>
  `;
}

function render(){
  const grid = document.getElementById('vendorsGrid');
  const search = document.getElementById('searchInput').value.toLowerCase();
  const cat = document.getElementById('categoryFilter').value.toLowerCase();
  const filtered = dummyVendors.filter(v=>{
    const text = `${v.business_name} ${v.name} ${v.category} ${v.city}`.toLowerCase();
    return (!cat || v.category.toLowerCase().includes(cat)) && (!search || text.includes(search));
  });
  grid.innerHTML = filtered.map(makeCard).join('');
  document.getElementById('noResults').classList.toggle('hidden', filtered.length>0);
  AOS.refresh();
}

document.addEventListener('DOMContentLoaded', ()=>{
  render();
  document.getElementById('searchBtn').onclick = render;
  document.getElementById('categoryFilter').onchange = render;

  const modal = document.getElementById('registerModal');
  document.getElementById('openRegister').onclick = ()=> modal.classList.remove('hidden');
  document.getElementById('closeRegister').onclick = ()=> modal.classList.add('hidden');

  document.getElementById('registerForm').onsubmit = (e)=>{
    e.preventDefault();
    alert("Registration form submitted (frontend only, backend coming soon).");
    modal.classList.add('hidden');
  };
});
