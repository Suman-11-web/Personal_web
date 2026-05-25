// --- JS ULTRA PRO MAX RECOGNITION ENGINE ---
async function getRealDeviceData() {
    let os = "Unknown OS";
    let browser = "Unknown Browser";
    let device = "Desktop / PC";
    let type = "Desktop";

    const ua = navigator.userAgent.toLowerCase();

    // 1. Get Browser
    if (ua.includes('edg/')) browser = "Edge";
    else if (ua.includes('opr/') || ua.includes('opera/')) browser = "Opera";
    else if (ua.includes('chrome/')) browser = "Chrome";
    else if (ua.includes('safari/') && !ua.includes('chrome')) browser = "Safari";
    else if (ua.includes('firefox/')) browser = "Firefox";

    // 2. High-Entropy Engine (Bypasses Android 10 Freeze on Modern Browsers)
    if (navigator.userAgentData) {
        type = navigator.userAgentData.mobile ? "Mobile" : "Desktop";
        try {
            // Request the deeply hidden hardware data
            const values = await navigator.userAgentData.getHighEntropyValues([
                "platform", "platformVersion", "model"
            ]);
            
            // Map the REAL Android/Windows version
            if (values.platform === "Android") {
                os = "Android " + values.platformVersion;
            } else if (values.platform === "Windows") {
                os = "Windows " + values.platformVersion;
            } else {
                os = values.platform;
            }

            // Map Specific Hardware Models
            if (values.model) {
                const m = values.model.toUpperCase();
                // Nothing Phone Logic
                if (m.includes('A063')) device = "Nothing Phone (1)";
                else if (m.includes('A065')) device = "Nothing Phone (2)";
                else if (m.includes('A142')) device = "Nothing Phone (2a)";
                else if (m.includes('A015')) device = "CMF Phone 1";
                // Samsung & Others
                else if (m.includes('SM-')) device = "Samsung Galaxy (" + values.model + ")";
                else if (m.includes('PIXEL')) device = "Google Pixel";
                else device = values.model; // Fallback to whatever the hardware reports
            } else {
                device = type === "Mobile" ? "Generic Android" : "Computer";
            }
        } catch (e) {
            console.warn("High Entropy Blocked:", e);
        }
    } 
    
    // 3. Fallback for older browsers / iOS (Apple doesn't support High Entropy)
    if (os === "Unknown OS" || os === "Android") {
        if (ua.includes('iphone')) {
            device = "Apple iPhone"; type = "Mobile";
            const match = ua.match(/os (\d+[_]\d+)/);
            os = match ? "iOS " + match[1].replace('_', '.') : "iOS";
        } else if (ua.includes('mac os')) {
            device = "Apple Mac"; os = "macOS";
        } else if (ua.includes('android')) {
            type = "Mobile";
            const match = ua.match(/android\s([0-9\.]+)/);
            os = match ? "Android " + match[1] : "Android";
            // Check UA for Nothing Phone just in case
            if (ua.includes('a063')) device = "Nothing Phone (1)";
            else if (ua.includes('a065')) device = "Nothing Phone (2)";
            else if (ua.includes('a142')) device = "Nothing Phone (2a)";
            else if (ua.includes('sm-')) device = "Samsung Galaxy";
        }
    }

    return { os, browser, device, type };
}

// 4. Send the data silently to Python backend
window.addEventListener('DOMContentLoaded', () => {
    // Check if it's a bot based on standard UA string to prevent spam
    const ua = navigator.userAgent.toLowerCase();
    const isBot = /bot|crawl|spider|slurp|googlebot|bingbot|yandex/.test(ua);
    
    if (!isBot) {
        getRealDeviceData().then(data => {
            fetch('/log_visitor', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).catch(err => console.log("Tracker silent fail:", err));
        });
    }
});
