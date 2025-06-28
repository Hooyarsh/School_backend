document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#invoiceForm");

  if (!form) {
    console.warn("Invoice form not found!");
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    console.log("🧾 Submitting form...");
    
    const jalaliDate = document.getElementById("invoice_date").value;
    const formattedJalaliDate = jalaliDate.replace(/\//g, '-');

    // Gather and send data using fetch:
    const formData = new FormData(form);
    const data = {
      invoice_number: document.getElementById("invoice_number").value,
      invoice_date: formattedJalaliDate,//document.getElementById("invoiceDate").value,
      total_amount: document.getElementById("total_amount").value,
      supplier_details: document.getElementById("supplier_details").value,
      description: document.getElementById("description").value,
      items: [],
};

    let i = 1;
    while (formData.get(`itemCount${i}`)) {
      data.items.push({
        count: document.getElementById(`itemCount${i}`).value,
        level: document.getElementById(`level${i}`).value,
        invoice_type: document.getElementById(`invoice_type${i}`).value,
        national_id: document.getElementById(`national_id${i}`)?.value || "",
        subgroup_language: document.getElementById(`subgroup_language${i}`)?.value || "",
        category: document.getElementById(`category${i}`).value,
        sub_code: document.getElementById(`sub_code${i}`).value,
        detail_code: document.getElementById(`detail_code${i}`).value,
        other_detail_code: document.getElementById(`other_detail_code${i}`)?.value || "",
        unit_price: document.getElementById(`unit_price${i}`).value,
      });

      i++;
    }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }




    fetch("/api/submit-invoice/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": getCookie('csrftoken'),
      },

      
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((response) => {
        alert("✅ داده‌ها با موفقیت ثبت شد.");
        form.reset();
      })
      .catch((err) => {
        console.error("❌ خطا در ارسال فرم:", err);
        alert("❌ خطا در ارسال فرم. لطفاً دوباره تلاش کنید.");
      });
  });
});
