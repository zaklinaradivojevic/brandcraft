 // BrandCraft.ai - Main JavaScript (Modern Version)

// DOM elementi
const generateBtn = document.getElementById('generateBtn');
const brandPrompt = document.getElementById('brandPrompt');
const demoResult = document.getElementById('demoResult');
const colorPreview = document.getElementById('colorPreview');
const fontPreview = document.getElementById('fontPreview');
const downloadBtn = document.getElementById('downloadPreviewBtn');

function generateColorsFromPrompt(prompt) {
    const lowerPrompt = prompt.toLowerCase();
    
    if (lowerPrompt.includes('industrial') || lowerPrompt.includes('brick')) {
        return { primary: '#C41E3A', secondary: '#2C2C2C', accent: '#D4AF37', light: '#F5F5F5', dark: '#1A1A1A' };
    }
    if (lowerPrompt.includes('modern') || lowerPrompt.includes('minimal') || lowerPrompt.includes('tech')) {
        return { primary: '#2D2D2D', secondary: '#F5F5F5', accent: '#00C2A0', light: '#FFFFFF', dark: '#000000' };
    }
    if (lowerPrompt.includes('vintage') || lowerPrompt.includes('rustic') || lowerPrompt.includes('book')) {
        return { primary: '#8B4513', secondary: '#F4ECD8', accent: '#CD853F', light: '#FFF8F0', dark: '#3E2723' };
    }
    if (lowerPrompt.includes('cozy') || lowerPrompt.includes('warm') || lowerPrompt.includes('cafe')) {
        return { primary: '#D2691E', secondary: '#FFE4B5', accent: '#FF6347', light: '#FFF5EE', dark: '#5C4033' };
    }
    if (lowerPrompt.includes('bold') || lowerPrompt.includes('energetic')) {
        return { primary: '#FF4757', secondary: '#2ED573', accent: '#FFA502', light: '#F1F2F6', dark: '#2F3542' };
    }
    return { primary: '#667eea', secondary: '#764ba2', accent: '#f093fb', light: '#f8f9fa', dark: '#343a40' };
}

function generateTagline(prompt) {
    const lowerPrompt = prompt.toLowerCase();
    if (lowerPrompt.includes('coffee')) return 'Fresh coffee, great vibes';
    if (lowerPrompt.includes('tech')) return 'Innovation meets design';
    if (lowerPrompt.includes('book')) return 'Stories that matter';
    return 'Your vibe, your brand';
}

function generateFonts(prompt) {
    const lowerPrompt = prompt.toLowerCase();
    if (lowerPrompt.includes('modern') || lowerPrompt.includes('tech')) {
        return { heading: 'Inter', body: 'Inter', headingStyle: 'bold, modern', bodyStyle: 'clean, minimal' };
    }
    if (lowerPrompt.includes('vintage') || lowerPrompt.includes('book')) {
        return { heading: 'Playfair Display', body: 'Lora', headingStyle: 'elegant, serif', bodyStyle: 'warm, readable' };
    }
    return { heading: 'Poppins', body: 'Open Sans', headingStyle: 'modern, friendly', bodyStyle: 'clean, readable' };
}

function displayColors(colors) {
    colorPreview.innerHTML = '';
    const previewDiv = document.getElementById('colorPreview');
    
    for (const [name, hex] of Object.entries(colors)) {
        const dot = document.createElement('div');
        dot.className = 'color-dot-modern';
        dot.style.backgroundColor = hex;
        dot.title = `${name}: ${hex}`;
        dot.addEventListener('click', () => {
            navigator.clipboard.writeText(hex);
            const originalTitle = dot.title;
            dot.title = 'Copied! ✓';
            setTimeout(() => { dot.title = originalTitle; }, 1000);
        });
        previewDiv.appendChild(dot);
    }
}

function displayFonts(fonts, tagline) {
    fontPreview.innerHTML = `
        <div style="background: rgba(255,255,255,0.08); border-radius: 16px; padding: 1rem;">
            <div style="margin-bottom: 0.5rem;">
                <span style="color: rgba(255,255,255,0.6); font-size: 0.7rem;">HEADING:</span>
                <p style="font-family: '${fonts.heading}', sans-serif; font-size: 1.1rem; font-weight: bold; margin: 0; color: white;">${fonts.heading}</p>
            </div>
            <div>
                <span style="color: rgba(255,255,255,0.6); font-size: 0.7rem;">BODY:</span>
                <p style="font-family: '${fonts.body}', sans-serif; font-size: 0.9rem; margin: 0; color: rgba(255,255,255,0.8);">${fonts.body}</p>
            </div>
            <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.1);">
                <p style="font-family: '${fonts.heading}', sans-serif; font-size: 0.9rem; font-weight: bold; color: white; margin: 0;">Your Brand Name</p>
                <p style="font-family: '${fonts.body}', sans-serif; font-size: 0.8rem; color: rgba(255,255,255,0.7); margin: 0;">${tagline}</p>
            </div>
        </div>
    `;
}

async function generateBrand() {
    const prompt = brandPrompt.value.trim();
    if (!prompt) {
        alert('✨ Please describe your brand vibe first!');
        brandPrompt.focus();
        return;
    }
    
    const originalText = generateBtn.querySelector('.btn-text').textContent;
    const btnIcon = generateBtn.querySelector('.btn-icon');
    
    generateBtn.querySelector('.btn-text').textContent = 'Creating your brand';
    btnIcon.textContent = '🎨';
    generateBtn.disabled = true;
    
    setTimeout(() => {
        const colors = generateColorsFromPrompt(prompt);
        const fonts = generateFonts(prompt);
        const tagline = generateTagline(prompt);
        
        displayColors(colors);
        displayFonts(fonts, tagline);
        demoResult.classList.add('show');
        
        demoResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        generateBtn.querySelector('.btn-text').textContent = originalText;
        btnIcon.textContent = '→';
        generateBtn.disabled = false;
    }, 1500);
}

function downloadPreview() {
    if (!demoResult.classList.contains('show')) {
        alert('Please generate a brand first!');
        return;
    }
    
    alert('📥 Pro feature: Full HD download available in Pro version ($19 one-time)\n\nGet vector SVG, high-res PNG, and complete brand kit!');
}

generateBtn.addEventListener('click', generateBrand);

brandPrompt.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        generateBrand();
    }
});

if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadPreview);
}

const proBtn = document.getElementById('proBtn');
if (proBtn) {
    proBtn.addEventListener('click', (e) => {
        e.preventDefault();
        alert('✨ BrandCraft.ai Pro\n\nGet full vector exports, social media kit, and priority support for just $19 one-time.\n\nComing soon! Contact: hello@brandcraft.ai');
    });
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Modern pricing buttons
const proBtnModern = document.getElementById('proBtnModern');
const enterpriseBtn = document.getElementById('enterpriseBtn');

if (proBtnModern) {
    proBtnModern.addEventListener('click', (e) => {
        e.preventDefault();
        alert('✨ BrandCraft.ai Pro\n\nGet full vector exports, social media kit, priority support, and lifetime updates for just $19 one-time.\n\n🚀 Coming soon! Sign up for early access: hello@brandcraft.ai');
    });
}

if (enterpriseBtn) {
    enterpriseBtn.addEventListener('click', (e) => {
        e.preventDefault();
        alert('🏢 Enterprise Plan\n\nPerfect for agencies and teams managing multiple brands.\n\nIncludes: 10+ brands, team collaboration, white-label export, API access.\n\n📧 Contact us: enterprise@brandcraft.ai');
    });
}

console.log('BrandCraft.ai - Modern version ready! 🎨✨'); 
