import React, { useState } from "react";

// PESU GJBC Map Chatbot
// Single-file React component (Tailwind CSS assumed available)
// Image source (local): /mnt/data/8b3b1ee7-3924-47bd-b940-050213295fd9.png

export default function PesuMapChatbot() {
  const mapUrl = "/mnt/data/8b3b1ee7-3924-47bd-b940-050213295fd9.png";

  // Simple set of POIs and short, relative directions extracted from the provided map image.
  // These are approximate relative directions (e.g., north/south/east/west on the cropped map).
  const poiDirections = {
    "PES University Central Library":
      "Located to the northwest of the campus crop. From Golden Jubilee Block, walk northwest across the open area to reach the Central Library.",
    "PESU Gym":
      "PESU Gym is near the top-center of the map (north). From GJBC head straight north across the courtyard.",
    "GJB Assessment Centre":
      "The GJB Assessment Centre appears slightly northwest of the Mechanical block. It's close to the Central Library.",
    "Mechanical(C)Block":
      "Mechanical (C) Block is near the center of the map — a useful central landmark to orient yourself.",
    "PES Badminton Court":
      "The Badminton Court is to the northeast of the Mechanical block on the map.",
    "Hornbill Coffee":
      "Hornbill Coffee appears on the right (east) side of the cropped map, useful as an east-side landmark.",
    "JV Technosoft Pvt":
      "JV Technosoft is on the southwest side of the shown area, below the Central Library.",
    "Golden Jubilee Block":
      "Golden Jubilee Block (GJBC) is located toward the bottom-right (southeast) of the image and is the main block labeled 'Golden Jubilee Block - PES UNIVERSITY'.",
    "PES GJB Basketball Court":
      "The Basketball Court is just below the Golden Jubilee Block on this crop — a useful marker for the south edge of the GJBC area.",
    "PESU GJB Food Court":
      "The GJB Food Court sits to the right/southeast near the Golden Jubilee Block and Hornbill Coffee.",
  };

  const poiList = Object.keys(poiDirections);

  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi — I'm the PESU map helper. Ask me where something is (e.g., 'Where is Hornbill Coffee?') or click a POI on the left." },
  ]);
  const [input, setInput] = useState("");

  function pushMessage(from, text) {
    setMessages((m) => [...m, { from, text }]);
  }

  function handleSubmit(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    pushMessage("user", text);
    respondTo(text);
    setInput("");
  }

  function respondTo(text) {
    const lower = text.toLowerCase();
    // Try exact POI match first
    for (const poi of poiList) {
      if (lower.includes(poi.toLowerCase())) {
        pushMessage("bot", `Directions to ${poi}: ${poiDirections[poi]}`);
        return;
      }
    }

    // Try keyword matching
    if (lower.includes("library")) {
      pushMessage("bot", `Directions to PES University Central Library: ${poiDirections["PES University Central Library"]}`);
      return;
    }
    if (lower.includes("gym")) {
      pushMessage("bot", `Directions to PESU Gym: ${poiDirections["PESU Gym"]}`);
      return;
    }
    if (lower.includes("gjb") || lower.includes("golden jubilee") || lower.includes("golden")) {
      pushMessage("bot", `Directions to Golden Jubilee Block: ${poiDirections["Golden Jubilee Block"]}`);
      return;
    }

    // fallback
    pushMessage(
      "bot",
      "Sorry — I don't have specific directions for that phrase. Try asking 'Where is [POI name]?' or click one of the POIs listed in the left panel."
    );
  }

  function handlePoiClick(poi) {
    pushMessage("user", `Show me ${poi}`);
    pushMessage("bot", `Directions to ${poi}: ${poiDirections[poi]}`);
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Left: POI list */}
      <aside className="w-72 bg-white border-r p-4">
        <h2 className="text-lg font-semibold mb-3">POIs — GJBC Map</h2>
        <p className="text-sm text-gray-600 mb-4">Click any POI to get quick directions in chat.</p>
        <ul className="space-y-2 overflow-auto" style={{ maxHeight: "60vh" }}>
          {poiList.map((poi) => (
            <li key={poi}>
              <button
                onClick={() => handlePoiClick(poi)}
                className="w-full text-left p-2 rounded hover:bg-gray-100"
              >
                <div className="font-medium">{poi}</div>
                <div className="text-xs text-gray-500">{poiDirections[poi].slice(0, 60)}...</div>
              </button>
            </li>
          ))}
        </ul>

        <div className="mt-6 text-xs text-gray-500">Map image source: uploaded campus crop.</div>
      </aside>

      {/* Center: Map */}
      <main className="flex-1 p-4">
        <div className="rounded shadow bg-white p-3 mb-4">
          <h3 className="font-semibold mb-2">Campus Map</h3>
          <div className="border rounded overflow-hidden">
            <img src={mapUrl} alt="PESU GJBC map crop" className="w-full object-contain" />
          </div>
        </div>

        {/* Chat area */}
        <div className="rounded shadow bg-white p-3">
          <h3 className="font-semibold mb-2">Map Chatbot</h3>
          <div className="h-72 overflow-y-auto border rounded p-3 bg-gray-50" id="chat-window">
            {messages.map((m, i) => (
              <div key={i} className={`mb-3 flex ${m.from === "bot" ? "justify-start" : "justify-end"}`}>
                <div
                  className={`max-w-xl p-2 rounded ${m.from === "bot" ? "bg-white border" : "bg-blue-500 text-white"}`}
                >
                  <div className="text-sm">{m.text}</div>
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="mt-3 flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about a location or directions..."
              className="flex-1 border rounded p-2"
            />
            <button className="px-4 py-2 rounded bg-blue-600 text-white">Send</button>
          </form>
        </div>
      </main>

      {/* Right: Quick tips */}
      <aside className="w-72 bg-white border-l p-4">
        <h2 className="text-lg font-semibold mb-3">Quick Tips</h2>
        <ol className="list-decimal pl-5 text-sm text-gray-700 space-y-2">
          <li>Click a POI on the left to auto-insert directions into the chat.</li>
          <li>Ask natural questions like "Where is Hornbill Coffee?" or "How do I get to the Library from GJBC?"</li>
          <li>If you need an exact indoor floor plan, contact campus facilities or the library — this map is a cropped overview.</li>
        </ol>

        <div className="mt-6 text-xs text-gray-500">Need changes? Tell me to add more POIs or make replies more detailed.</div>
      </aside>
    </div>
  );
}
