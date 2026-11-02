import os

assets = {
    'headphones.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#EEF2FF"/>
      <stop offset="100%" stop-color="#E0E7FF"/>
    </radialGradient>
    <linearGradient id="bandGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="goldAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <linearGradient id="cupGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="18" stdDeviation="15" flood-color="#0f172a" flood-opacity="0.18"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlow)"/>
  
  <g filter="url(#softShadow)">
    <!-- Headband Arch -->
    <path d="M 180 340 C 180 160, 420 160, 420 340" fill="none" stroke="url(#bandGrad)" stroke-width="38" stroke-linecap="round"/>
    <path d="M 210 240 C 240 180, 360 180, 390 240" fill="none" stroke="url(#goldAccent)" stroke-width="6" stroke-linecap="round"/>

    <!-- Left Ear Cup Structure -->
    <g transform="translate(140, 290)">
      <rect x="0" y="20" width="46" height="130" rx="23" fill="url(#bandGrad)"/>
      <rect x="25" y="0" width="42" height="170" rx="21" fill="url(#cupGrad)"/>
      <rect x="35" y="30" width="10" height="110" rx="5" fill="url(#goldAccent)"/>
      <circle cx="45" cy="85" r="16" fill="#1E293B"/>
      <circle cx="45" cy="85" r="8" fill="#F59E0B"/>
    </g>

    <!-- Right Ear Cup Structure -->
    <g transform="translate(390, 290)">
      <rect x="26" y="20" width="46" height="130" rx="23" fill="url(#bandGrad)"/>
      <rect x="5" y="0" width="42" height="170" rx="21" fill="url(#cupGrad)"/>
      <rect x="27" y="30" width="10" height="110" rx="5" fill="url(#goldAccent)"/>
      <circle cx="27" cy="85" r="16" fill="#1E293B"/>
      <circle cx="27" cy="85" r="8" fill="#F59E0B"/>
    </g>
  </g>
  <!-- Modern Tech Badge -->
  <g transform="translate(420, 50)">
    <rect width="130" height="36" rx="18" fill="#4F46E5" fill-opacity="0.12"/>
    <text x="65" y="23" fill="#4F46E5" font-family="system-ui, sans-serif" font-weight="700" font-size="14" text-anchor="middle">Hi-Res Audio</text>
  </g>
</svg>''',

    'smartwatch.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowWatch" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F0FDF4"/>
      <stop offset="100%" stop-color="#DCFCE7"/>
    </radialGradient>
    <linearGradient id="strapGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="dialGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E1E24"/>
      <stop offset="100%" stop-color="#090A0F"/>
    </linearGradient>
    <filter id="watchShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.2"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowWatch)"/>
  
  <g filter="url(#watchShadow)" transform="translate(160, 50)">
    <!-- Top Strap -->
    <path d="M 60 0 L 220 0 L 205 150 L 75 150 Z" fill="url(#strapGrad)"/>
    <!-- Bottom Strap -->
    <path d="M 75 350 L 205 350 L 220 500 L 60 500 Z" fill="url(#strapGrad)"/>

    <!-- Case Outline -->
    <rect x="35" y="125" width="210" height="250" rx="55" fill="#334155"/>
    <rect x="45" y="135" width="190" height="230" rx="45" fill="url(#dialGrad)" stroke="#475569" stroke-width="4"/>
    
    <!-- Crown Button -->
    <rect x="245" y="195" width="14" height="45" rx="7" fill="#64748B"/>
    <rect x="245" y="270" width="10" height="35" rx="5" fill="#475569"/>

    <!-- Screen UI Elements -->
    <text x="140" y="220" fill="#FFFFFF" font-family="system-ui, sans-serif" font-weight="800" font-size="52" text-anchor="middle">10:42</text>
    <text x="140" y="250" fill="#10B981" font-family="system-ui, sans-serif" font-weight="600" font-size="16" text-anchor="middle">THU, OCT 28</text>
    
    <!-- Activity Rings -->
    <circle cx="140" cy="305" r="32" fill="none" stroke="#1E293B" stroke-width="8"/>
    <circle cx="140" cy="305" r="32" fill="none" stroke="#EF4444" stroke-width="8" stroke-dasharray="140 200" stroke-linecap="round"/>
    <circle cx="140" cy="305" r="20" fill="none" stroke="#10B981" stroke-width="8" stroke-dasharray="90 150" stroke-linecap="round"/>
  </g>
</svg>''',

    'laptop.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowLap" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </radialGradient>
    <linearGradient id="aluminum" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E2E8F0"/>
      <stop offset="50%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#94A3B8"/>
    </linearGradient>
    <linearGradient id="screenWallpaper" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4F46E5"/>
      <stop offset="50%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>
    <filter id="lapShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="22" stdDeviation="18" flood-color="#0f172a" flood-opacity="0.18"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowLap)"/>
  
  <g filter="url(#lapShadow)" transform="translate(60, 110)">
    <!-- Screen Lid -->
    <rect x="70" y="20" width="340" height="225" rx="16" fill="#0F172A"/>
    <!-- Glass Display -->
    <rect x="82" y="32" width="316" height="198" rx="8" fill="url(#screenWallpaper)"/>
    <!-- Web Camera dot -->
    <circle cx="240" cy="26" r="3" fill="#334155"/>
    <circle cx="240" cy="26" r="1" fill="#38BDF8"/>
    <!-- Screen Accent Art -->
    <circle cx="330" cy="110" r="50" fill="#FFFFFF" fill-opacity="0.15"/>
    <path d="M 100 190 Q 200 100, 320 180 T 380 150" fill="none" stroke="#FFFFFF" stroke-opacity="0.4" stroke-width="3"/>

    <!-- Bottom Base / Body -->
    <path d="M 20 250 L 460 250 L 440 280 L 40 280 Z" fill="url(#aluminum)"/>
    <rect x="180" y="252" width="120" height="6" rx="3" fill="#64748B"/>
    <!-- Laptop Front Lip -->
    <rect x="25" y="278" width="430" height="10" rx="4" fill="#94A3B8"/>
  </g>
</svg>''',

    'shoes.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowShoes" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF1F2"/>
      <stop offset="100%" stop-color="#FFE4E6"/>
    </radialGradient>
    <linearGradient id="shoeBody" x1="0%" y1="0%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="50%" stop-color="#F43F5E"/>
      <stop offset="100%" stop-color="#FB7185"/>
    </linearGradient>
    <linearGradient id="soleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
    <filter id="shoeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#881337" flood-opacity="0.18"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowShoes)"/>
  
  <g filter="url(#shoeShadow)" transform="translate(60, 160)">
    <!-- Sole Bottom -->
    <path d="M 40 230 C 120 235, 340 235, 430 200 C 455 190, 460 170, 440 180 C 370 210, 150 200, 40 210 Z" fill="#0F172A"/>
    <!-- Cushion Midsole -->
    <path d="M 40 210 C 130 215, 330 215, 440 180 C 450 160, 420 155, 380 165 C 280 185, 120 175, 40 190 Z" fill="url(#soleGrad)"/>
    
    <!-- Shoe Upper Mesh -->
    <path d="M 40 190 C 50 130, 90 90, 160 85 C 200 85, 230 110, 270 140 C 320 150, 400 155, 420 160 C 420 170, 390 170, 380 165 C 320 170, 120 175, 40 190 Z" fill="url(#shoeBody)"/>
    
    <!-- Dynamic Swoosh / Wave -->
    <path d="M 120 160 Q 220 120, 310 155 Q 230 145, 140 180 Z" fill="#FFFFFF"/>
    
    <!-- Heel Collar & Tongue -->
    <path d="M 130 90 C 150 50, 190 70, 210 100 C 190 100, 150 95, 130 90 Z" fill="#1E293B"/>
    
    <!-- Laces Details -->
    <line x1="180" y1="105" x2="220" y2="125" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
    <line x1="195" y1="120" x2="235" y2="135" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
    <line x1="210" y1="135" x2="250" y2="145" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  </g>
</svg>''',

    'bag.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowBag" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="100%" stop-color="#FDE68A"/>
    </radialGradient>
    <linearGradient id="leather" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#B45309"/>
      <stop offset="50%" stop-color="#92400E"/>
      <stop offset="100%" stop-color="#78350F"/>
    </linearGradient>
    <linearGradient id="brass" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDE047"/>
      <stop offset="100%" stop-color="#CA8A04"/>
    </linearGradient>
    <filter id="bagShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#78350F" flood-opacity="0.25"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowBag)"/>
  
  <g filter="url(#bagShadow)" transform="translate(100, 100)">
    <!-- Shoulder Strap Arc -->
    <path d="M 40 200 C 40 20, 360 20, 360 200" fill="none" stroke="#78350F" stroke-width="18" stroke-linecap="round"/>
    
    <!-- Top Handle -->
    <path d="M 140 140 C 140 90, 260 90, 260 140" fill="none" stroke="#B45309" stroke-width="16" stroke-linecap="round"/>
    <rect x="132" y="135" width="16" height="24" rx="4" fill="url(#brass)"/>
    <rect x="252" y="135" width="16" height="24" rx="4" fill="url(#brass)"/>

    <!-- Main Bag Body -->
    <rect x="30" y="150" width="340" height="230" rx="24" fill="url(#leather)"/>
    <!-- Front Flap Overhang -->
    <path d="M 30 150 L 370 150 L 360 290 C 260 320, 140 320, 40 290 Z" fill="#78350F"/>
    
    <!-- Leather Straps & Brass Buckles -->
    <rect x="90" y="150" width="22" height="180" rx="6" fill="#B45309"/>
    <rect x="85" y="270" width="32" height="42" rx="6" fill="url(#brass)"/>
    <rect x="93" y="278" width="16" height="26" rx="3" fill="#78350F"/>

    <rect x="288" y="150" width="22" height="180" rx="6" fill="#B45309"/>
    <rect x="283" y="270" width="32" height="42" rx="6" fill="url(#brass)"/>
    <rect x="291" y="278" width="16" height="26" rx="3" fill="#78350F"/>
  </g>
</svg>''',

    'backpack.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowPack" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F1F5F9"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </radialGradient>
    <linearGradient id="packGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <filter id="packShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#0F172A" flood-opacity="0.2"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowPack)"/>
  
  <g filter="url(#packShadow)" transform="translate(130, 80)">
    <!-- Top Carry Handle -->
    <path d="M 130 60 C 130 20, 210 20, 210 60" fill="none" stroke="#64748B" stroke-width="12" stroke-linecap="round"/>

    <!-- Main Silhouette -->
    <path d="M 70 420 C 50 420, 40 370, 50 160 C 60 70, 120 40, 170 40 C 220 40, 280 70, 290 160 C 300 370, 290 420, 270 420 Z" fill="url(#packGrad)"/>
    
    <!-- Front Compartment Pocket -->
    <path d="M 70 230 C 70 200, 270 200, 270 230 L 260 390 C 260 410, 80 410, 80 390 Z" fill="#1E293B" stroke="#475569" stroke-width="2"/>
    
    <!-- Minimalist Orange Zip Puller -->
    <rect x="80" y="240" width="180" height="4" rx="2" fill="#475569"/>
    <circle cx="240" cy="242" r="7" fill="#F97316"/>
    
    <!-- Water Bottle Mesh Side Pocket -->
    <path d="M 45 280 C 40 280, 40 380, 55 390 L 75 390 L 70 280 Z" fill="#475569" opacity="0.7"/>
    <!-- Brand Tag -->
    <rect x="150" y="340" width="40" height="16" rx="4" fill="#0F172A"/>
    <rect x="160" y="346" width="20" height="4" rx="2" fill="#F97316"/>
  </g>
</svg>''',

    'keyboard.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowKb" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FAF5FF"/>
      <stop offset="100%" stop-color="#F3E8FF"/>
    </radialGradient>
    <linearGradient id="rgbBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8B5CF6"/>
      <stop offset="50%" stop-color="#EC4899"/>
      <stop offset="100%" stop-color="#3B82F6"/>
    </linearGradient>
    <filter id="kbShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#581C87" flood-opacity="0.18"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowKb)"/>
  
  <g filter="url(#kbShadow)" transform="translate(60, 160)">
    <!-- Base Plate with RGB Rim -->
    <rect x="0" y="0" width="480" height="260" rx="20" fill="url(#rgbBorder)"/>
    <rect x="6" y="6" width="468" height="248" rx="16" fill="#0F172A"/>

    <!-- Keycap Matrix Rows -->
    <!-- Row 1 -->
    <g fill="#1E293B" stroke="#334155" stroke-width="1.5">
      <rect x="25" y="25" width="30" height="30" rx="5" fill="#EF4444"/>
      <rect x="62" y="25" width="28" height="30" rx="5"/>
      <rect x="96" y="25" width="28" height="30" rx="5"/>
      <rect x="130" y="25" width="28" height="30" rx="5"/>
      <rect x="164" y="25" width="28" height="30" rx="5"/>
      <rect x="198" y="25" width="28" height="30" rx="5"/>
      <rect x="232" y="25" width="28" height="30" rx="5"/>
      <rect x="266" y="25" width="28" height="30" rx="5"/>
      <rect x="300" y="25" width="28" height="30" rx="5"/>
      <rect x="334" y="25" width="28" height="30" rx="5"/>
      <rect x="368" y="25" width="28" height="30" rx="5"/>
      <rect x="402" y="25" width="53" height="30" rx="5" fill="#3B82F6"/>

      <!-- Row 2 -->
      <rect x="25" y="62" width="42" height="30" rx="5"/>
      <rect x="73" y="62" width="28" height="30" rx="5"/>
      <rect x="107" y="62" width="28" height="30" rx="5"/>
      <rect x="141" y="62" width="28" height="30" rx="5"/>
      <rect x="175" y="62" width="28" height="30" rx="5"/>
      <rect x="209" y="62" width="28" height="30" rx="5"/>
      <rect x="243" y="62" width="28" height="30" rx="5"/>
      <rect x="277" y="62" width="28" height="30" rx="5"/>
      <rect x="311" y="62" width="28" height="30" rx="5"/>
      <rect x="345" y="62" width="28" height="30" rx="5"/>
      <rect x="379" y="62" width="28" height="30" rx="5"/>
      <rect x="413" y="62" width="42" height="30" rx="5"/>

      <!-- Row 3 Home Row -->
      <rect x="25" y="99" width="50" height="30" rx="5"/>
      <rect x="81" y="99" width="28" height="30" rx="5"/>
      <rect x="115" y="99" width="28" height="30" rx="5"/>
      <rect x="149" y="99" width="28" height="30" rx="5"/>
      <rect x="183" y="99" width="28" height="30" rx="5"/>
      <rect x="217" y="99" width="28" height="30" rx="5"/>
      <rect x="251" y="99" width="28" height="30" rx="5"/>
      <rect x="285" y="99" width="28" height="30" rx="5"/>
      <rect x="319" y="99" width="28" height="30" rx="5"/>
      <rect x="353" y="99" width="28" height="30" rx="5"/>
      <rect x="387" y="99" width="68" height="30" rx="5" fill="#8B5CF6"/>

      <!-- Row 4 Spacebar Row -->
      <rect x="25" y="136" width="60" height="30" rx="5"/>
      <rect x="91" y="136" width="28" height="30" rx="5"/>
      <rect x="125" y="136" width="28" height="30" rx="5"/>
      <rect x="159" y="136" width="28" height="30" rx="5"/>
      <rect x="193" y="136" width="28" height="30" rx="5"/>
      <rect x="227" y="136" width="28" height="30" rx="5"/>
      <rect x="261" y="136" width="28" height="30" rx="5"/>
      <rect x="295" y="136" width="28" height="30" rx="5"/>
      <rect x="329" y="136" width="28" height="30" rx="5"/>
      <rect x="363" y="136" width="92" height="30" rx="5"/>

      <!-- Spacebar -->
      <rect x="135" y="173" width="190" height="32" rx="6" fill="#6366F1"/>
      <rect x="25" y="173" width="45" height="32" rx="6"/>
      <rect x="76" y="173" width="45" height="32" rx="6"/>
      <rect x="339" y="173" width="45" height="32" rx="6"/>
      <rect x="390" y="173" width="65" height="32" rx="6"/>
    </g>
  </g>
</svg>''',

    'sunglasses.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowSun" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FEFCE8"/>
      <stop offset="100%" stop-color="#FEF08A"/>
    </radialGradient>
    <linearGradient id="lensGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="70%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#3B82F6"/>
    </linearGradient>
    <linearGradient id="goldFrame" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FDE047"/>
      <stop offset="50%" stop-color="#EAB308"/>
      <stop offset="100%" stop-color="#CA8A04"/>
    </linearGradient>
    <filter id="sunShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#854D0E" flood-opacity="0.2"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowSun)"/>
  
  <g filter="url(#sunShadow)" transform="translate(60, 190)">
    <!-- Bridge Bar Top -->
    <path d="M 170 30 Q 240 10, 310 30" fill="none" stroke="url(#goldFrame)" stroke-width="8" stroke-linecap="round"/>
    <path d="M 210 65 Q 240 55, 270 65" fill="none" stroke="url(#goldFrame)" stroke-width="6" stroke-linecap="round"/>

    <!-- Left Teardrop Aviator Lens -->
    <path d="M 60 40 C 180 30, 210 60, 210 130 C 210 200, 130 220, 80 160 C 50 120, 40 50, 60 40 Z" fill="url(#lensGrad)" stroke="url(#goldFrame)" stroke-width="8"/>
    <!-- Glass Highlight Reflection -->
    <path d="M 90 60 C 140 55, 170 80, 160 120" fill="none" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="4" stroke-linecap="round"/>

    <!-- Right Teardrop Aviator Lens -->
    <path d="M 420 40 C 300 30, 270 60, 270 130 C 270 200, 350 220, 400 160 C 430 120, 440 50, 420 40 Z" fill="url(#lensGrad)" stroke="url(#goldFrame)" stroke-width="8"/>
    <!-- Glass Highlight Reflection -->
    <path d="M 390 60 C 340 55, 310 80, 320 120" fill="none" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="4" stroke-linecap="round"/>

    <!-- Frame Temple Hinges -->
    <rect x="35" y="36" width="20" height="8" rx="4" fill="url(#goldFrame)"/>
    <rect x="425" y="36" width="20" height="8" rx="4" fill="url(#goldFrame)"/>
  </g>
</svg>''',

    'sneakers.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowSneak" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#EFF6FF"/>
      <stop offset="100%" stop-color="#DBEAFE"/>
    </radialGradient>
    <filter id="sneakShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#1E3A8A" flood-opacity="0.18"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowSneak)"/>
  
  <g filter="url(#sneakShadow)" transform="translate(60, 170)">
    <!-- Thick Rubber Sole -->
    <rect x="40" y="210" width="410" height="38" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="3"/>
    <line x1="40" y1="225" x2="450" y2="225" stroke="#EF4444" stroke-width="3"/>
    
    <!-- Canvas Upper -->
    <path d="M 40 210 C 40 140, 90 90, 160 90 L 260 140 C 340 150, 420 180, 450 210 Z" fill="#1E3A8A"/>
    <!-- Rubber Toe Cap -->
    <path d="M 400 210 C 430 200, 450 200, 450 210 Z" fill="#FFFFFF"/>
    <path d="M 390 210 C 390 180, 430 180, 450 210 Z" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>

    <!-- Ankle Star Badge -->
    <circle cx="120" cy="140" r="28" fill="#FFFFFF"/>
    <path d="M 120 124 L 124 135 L 135 135 L 126 142 L 130 153 L 120 146 L 110 153 L 114 142 L 105 135 L 116 135 Z" fill="#1E3A8A"/>

    <!-- Clean White Laces -->
    <line x1="190" y1="120" x2="230" y2="150" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <line x1="220" y1="140" x2="260" y2="165" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <line x1="250" y1="160" x2="290" y2="180" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  </g>
</svg>''',

    'waterbottle.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGlowBot" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ECFDF5"/>
      <stop offset="100%" stop-color="#D1FAE5"/>
    </radialGradient>
    <linearGradient id="steel" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="40%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <filter id="botShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="20" stdDeviation="16" flood-color="#064E3B" flood-opacity="0.2"/>
    </filter>
  </defs>
  <rect width="600" height="600" rx="32" fill="url(#bgGlowBot)"/>
  
  <g filter="url(#botShadow)" transform="translate(200, 60)">
    <!-- Loop Cap Handle -->
    <path d="M 70 50 C 70 10, 130 10, 130 50" fill="none" stroke="#0F172A" stroke-width="16" stroke-linecap="round"/>
    <!-- Stainless Cap -->
    <rect x="65" y="50" width="70" height="35" rx="8" fill="#334155"/>
    <rect x="75" y="85" width="50" height="15" fill="#64748B"/>

    <!-- Bottle Neck -->
    <path d="M 70 100 L 130 100 L 160 150 L 40 150 Z" fill="url(#steel)"/>

    <!-- Main Insulated Cylinder Body -->
    <rect x="40" y="150" width="120" height="310" rx="20" fill="url(#steel)"/>
    
    <!-- Light Reflection Strip -->
    <rect x="60" y="150" width="14" height="300" rx="7" fill="#FFFFFF" fill-opacity="0.25"/>

    <!-- Temperature Display Ring -->
    <rect x="65" y="240" width="70" height="30" rx="15" fill="#064E3B"/>
    <text x="100" y="261" fill="#6EE7B7" font-family="system-ui, sans-serif" font-weight="700" font-size="14" text-anchor="middle">5°C COLD</text>
  </g>
</svg>''',

    'placeholder.svg': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
  <rect width="600" height="600" rx="32" fill="#F1F5F9"/>
  <circle cx="300" cy="270" r="80" fill="#E2E8F0"/>
  <path d="M 270 250 L 330 250 L 300 290 Z" fill="#94A3B8"/>
  <text x="300" y="390" fill="#64748B" font-family="system-ui, sans-serif" font-weight="600" font-size="22" text-anchor="middle">ShopEase Product</text>
</svg>'''
}

dest_dir = r"C:\Users\Welcome\.gemini\antigravity-ide\scratch\EcommerceStore\static\images\products"
os.makedirs(dest_dir, exist_ok=True)

for fname, content in assets.items():
    fpath = os.path.join(dest_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"Created {fname}")
