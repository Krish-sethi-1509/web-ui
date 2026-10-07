(function ($) {
  "use strict";

  var laptops = [];
  var visibleLimit = 24;
  var selected = new Set();
  var filters = { query: "", brand: "", category: "", budget: Infinity, ram: 0, sort: "recommended" };

  function text(value, fallback) {
    if (value === null || value === undefined || String(value).trim() === "") return fallback || "Not listed";
    return String(value);
  }

  function money(value) {
    var amount = Number(value);
    return Number.isFinite(amount) ? "₹" + amount.toLocaleString("en-IN", { maximumFractionDigits: 0 }) : "Price unavailable";
  }

  function setStatus(message, isError) {
    $("#load-message").text(message).toggleClass("error", Boolean(isError)).prop("hidden", !message);
  }

  function populateBrands() {
    var brands = Array.from(new Set(laptops.map(function (item) { return text(item.brand, "").trim(); }).filter(Boolean)));
    brands.sort(function (a, b) { return a.localeCompare(b); });
    brands.forEach(function (brand) { $("#brand").append($("<option>").val(brand).text(brand)); });
  }

  function filteredLaptops() {
    var matches = laptops.filter(function (item) {
      var searchText = (text(item.brand, "") + " " + text(item.model, "")).toLowerCase();
      return (!filters.query || searchText.indexOf(filters.query) !== -1) &&
        (!filters.brand || text(item.brand, "") === filters.brand) &&
        (!filters.category || text(item.device_category, "") === filters.category) &&
        (!Number.isFinite(Number(item.price)) || Number(item.price) <= filters.budget) &&
        Number(item.ram_gb || 0) >= filters.ram;
    });

    if (filters.sort === "price-low") matches.sort(function (a, b) { return Number(a.price || Infinity) - Number(b.price || Infinity); });
    if (filters.sort === "price-high") matches.sort(function (a, b) { return Number(b.price || 0) - Number(a.price || 0); });
    if (filters.sort === "rating") matches.sort(function (a, b) { return Number(b.rating || 0) - Number(a.rating || 0); });
    return matches;
  }

  function spec(label, value) {
    var cell = $("<div>");
    cell.append($("<dt>").text(label), $("<dd>").text(value));
    return cell;
  }

  function makeCard(item) {
    var card = $("<article>").addClass("product-card");
    var top = $("<div>").addClass("card-top");
    top.append($("<span>").addClass("brand-name").text(text(item.brand, "Unknown brand")));
    top.append($("<span>").addClass("category-tag").text(text(item.device_category, "General")));
    card.append(top);
    card.append($("<h3>").text(text(item.model, "Laptop model not listed")));
    card.append($("<div>").addClass("price").text(money(item.price)));
    card.append($("<p>").addClass("price-caption").text("Dataset listed price"));
    var specs = $("<dl>").addClass("spec-list");
    specs.append(spec("Processor", text(item.cpu_series, text(item.cpu_brand))));
    specs.append(spec("Graphics", text(item.gpu_model, text(item.gpu_type))));
    specs.append(spec("Memory", text(item.ram_gb, "—") + (item.ram_gb ? " GB RAM" : "")));
    specs.append(spec("Storage", text(item.storage_gb, "—") + (item.storage_gb ? " GB" : "")));
    specs.append(spec("Screen", text(item.display_size_inch, "—") + (item.display_size_inch ? " in" : "")));
    specs.append(spec("Dataset rating", text(item.rating, "—") + (item.rating ? " / 100" : "")));
    card.append(specs);

    var actions = $("<div>").addClass("card-actions");
    var check = $("<input>").attr({ type: "checkbox", "aria-label": "Add " + text(item.model, "laptop") + " to comparison" });
    check.prop("checked", selected.has(item._index)).on("change", function () {
      if (this.checked && selected.size >= 3) {
        this.checked = false;
        $("#compare-hint").text("Compare up to three laptops at a time.");
        return;
      }
      if (this.checked) selected.add(item._index);
      else selected.delete(item._index);
      updateCompareBar();
    });
    actions.append($("<label>").addClass("compare-option").append(check, document.createTextNode("Compare")));
    card.append(actions);

    var details = $("<details>");
    var detailText = "Processor model: " + text(item.cpu_model) + " · Graphics: " + text(item.gpu_model) +
      " · Operating system: " + text(item.os_name) + " · Warranty: " + text(item.warranty_years, "Not listed");
    details.append($("<summary>").text("More specifications"));
    details.append($("<p>").addClass("details-copy").text(detailText));
    card.append(details);
    return card;
  }

  function render() {
    var matches = filteredLaptops();
    var shown = matches.slice(0, visibleLimit);
    var grid = $("#product-grid").empty();
    shown.forEach(function (item) { grid.append(makeCard(item)); });

    $("#result-count").text(matches.length.toLocaleString("en-IN") + " matching laptops");
    $("#empty-message").prop("hidden", matches.length !== 0);
    $("#show-more").prop("hidden", matches.length <= visibleLimit);
    $("#show-more").text("Show more (" + Math.min(24, matches.length - visibleLimit) + ")");
  }

  function updateCompareBar() {
    var count = selected.size;
    $("#compare-count").text(count + (count === 1 ? " selected" : " selected"));
    $("#compare-hint").text(count === 0 ? "Choose up to three laptops to compare" : "Select " + Math.max(0, 2 - count) + " more to compare");
    $("#compare-button").prop("disabled", count < 2);
  }

  function renderComparison() {
    var chosen = laptops.filter(function (item) { return selected.has(item._index); });
    var rows = [
      ["Brand", "brand"], ["Model", "model"], ["Price", "price"], ["Type", "device_category"],
      ["Processor", "cpu_model"], ["Graphics", "gpu_model"], ["RAM (GB)", "ram_gb"],
      ["Storage (GB)", "storage_gb"], ["Screen (inches)", "display_size_inch"], ["Rating (0–100)", "rating"]
    ];
    var table = $("<table>");
    var head = $("<tr>").append($("<th>").text("Specification"));
    chosen.forEach(function (item) { head.append($("<th>").text(text(item.model, "Laptop"))); });
    table.append($("<thead>").append(head));
    var body = $("<tbody>");
    rows.forEach(function (row) {
      var tr = $("<tr>").append($("<td>").text(row[0]));
      chosen.forEach(function (item) {
        var value = row[1] === "price" ? money(item.price) : text(item[row[1]]);
        tr.append($("<td>").text(value));
      });
      body.append(tr);
    });
    table.append(body);
    $("#comparison-table").empty().append(table);
    $("#comparison").prop("hidden", false);
    $("#comparison").get(0).scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function syncFilters() {
    filters.query = $("#search").val().trim().toLowerCase();
    filters.brand = $("#brand").val();
    filters.category = $("#category").val();
    filters.budget = Number($("#budget").val());
    filters.ram = Number($("#ram").val());
    filters.sort = $("#sort").val();
    $("#budget-value").text(filters.budget >= Number($("#budget").attr("max")) ? "Any price" : money(filters.budget));
    $("#ram-value").text(filters.ram ? filters.ram + " GB+" : "Any");
    visibleLimit = 24;
    render();
  }

  function loadCatalogue() {
    setStatus("Loading laptop listings with Ajax…", false);
    $.ajax({
      url: "../data/processed/laptops_cleaned.csv",
      method: "GET",
      dataType: "text",
      cache: true
    }).done(function (csv) {
      var parsed = Papa.parse(csv, { header: true, skipEmptyLines: true, dynamicTyping: true });
      if (parsed.errors.length) {
        setStatus("Some rows could not be read. Check the dataset CSV before presenting.", true);
        return;
      }
      laptops = parsed.data.map(function (item, index) {
        item._index = index;
        return item;
      }).filter(function (item) { return item.model && Number.isFinite(Number(item.price)); });

      if (!laptops.length) {
        setStatus("No usable laptop listings were found in the dataset.", true);
        return;
      }

      var maxPrice = Math.max.apply(null, laptops.map(function (item) { return Number(item.price); }));
      var roundedMax = Math.ceil(maxPrice / 10000) * 10000;
      $("#budget").attr("max", roundedMax).val(roundedMax);
      $("#budget-value").text("Any price");
      populateBrands();
      setStatus("", false);
      syncFilters();
    }).fail(function (xhr) {
      setStatus("Could not load the dataset (" + xhr.status + "). Start a local web server from the project root and open /web/.", true);
      $("#result-count").text("Listings unavailable");
    });
  }

  $(function () {
    $("#search, #brand, #category, #budget, #ram, #sort").on("input change", syncFilters);
    $("#clear-filters").on("click", function () {
      $("#search").val("");
      $("#brand, #category").val("");
      $("#ram").val("0");
      $("#budget").val($("#budget").attr("max"));
      $("#sort").val("recommended");
      syncFilters();
    });
    $("#show-more").on("click", function () {
      visibleLimit += 24;
      render();
    });
    $("#compare-button").on("click", renderComparison);
    $("#close-comparison").on("click", function () { $("#comparison").prop("hidden", true); });
    loadCatalogue();
  });
})(jQuery);