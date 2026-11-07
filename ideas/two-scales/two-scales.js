// Banked from the Gregory timeline studies (November 2026): "Two scales".
// His life (1870-1955) gets ~76% of the width, the legacy (1965-2030) folds behind a break mark;
// year labels fan out on leader lines so every year can be read. Click or hover a dot to fill the card.
// Expects: EV = [{y, t, d, c, p}] (year, title, detail, kind, place), helpers C(kind), esc(), key(),
// section(title, why, html) and wireDots(section, selector) as in two-scales-page.html.
/* 1 two scales */
(function(){
  var W=900,L0=1870,L1=1955,G0=1965,G1=2030,split=0.76,pad=20,brk=26;
  var lw=(W-2*pad-brk)*split, gw=(W-2*pad-brk)-lw;
  function X(y){return y<=L1?pad+lw*(y-L0)/(L1-L0):pad+lw+brk+gw*(y-G0)/(G1-G0)}
  var p=[];
  p.push('<rect x="'+X(1874)+'" y="66" width="'+(X(1951)-X(1874))+'" height="10" rx="5" fill="'+C('teach')+'" opacity=".16"/>');
  p.push('<text x="'+((X(1874)+X(1951))/2)+'" y="18" text-anchor="middle" class="era">His life, 1874–1951</text>');
  p.push('<text x="'+((X(1972)+X(2026))/2)+'" y="18" text-anchor="middle" class="era">The legacy</text>');
  p.push('<line x1="'+pad+'" y1="71" x2="'+(pad+lw)+'" y2="71" stroke="var(--rule)" stroke-width="2"/><line x1="'+(pad+lw+brk)+'" y1="71" x2="'+(W-pad)+'" y2="71" stroke="var(--rule)" stroke-width="2"/>');
  p.push('<path d="M'+(pad+lw+6)+' 79 l6 -16 M'+(pad+lw+14)+' 79 l6 -16" stroke="var(--mute)" stroke-width="1.5"/>');
  [1870,1880,1890,1900,1910,1920,1930,1940,1950].forEach(function(t){p.push('<text x="'+X(t)+'" y="40" text-anchor="middle" class="tk">'+t+'</text>')});
  
  var xs=EV.map(function(e){return X(e.y)}),lx=[],SP=31;
  xs.forEach(function(x,i){lx[i]=Math.max(x,i?lx[i-1]+SP:pad)});
  for(var i=xs.length-1;i>=0;i--){var lim=i<xs.length-1?lx[i+1]-SP:W-pad;if(lx[i]>lim)lx[i]=lim}
  for(var i=1;i<xs.length;i++)if(lx[i]<lx[i-1]+SP)lx[i]=lx[i-1]+SP;
  EV.forEach(function(e,i){var x=xs[i];p.push('<path d="M'+x+' 79 V90 L'+lx[i]+' 108 V112" fill="none" stroke="var(--rule)" stroke-width="1"/>')});
  EV.forEach(function(e,i){var x=xs[i];p.push('<circle class="dot" tabindex="0" role="button" aria-label="'+e.y+': '+esc(e.t)+'" data-i="'+i+'" cx="'+x+'" cy="71" r="6.5" fill="'+C(e.c)+'"/><text x="'+lx[i]+'" y="126" text-anchor="middle" class="yl" style="fill:'+C(e.c)+'">'+e.y+'</text>')});
  var s=section('1. Two scales','His seventy-seven years get three-quarters of the width, so the crowded years around 1910 open up; the decades after 1951 fold behind a break mark. Labels fan out beneath the line so every year can be read.',key()+'<svg viewBox="0 0 '+W+' 136">'+p.join('')+'</svg><div class="card"></div>');
  wireDots(s,'.dot');
})();

