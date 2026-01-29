(function(){
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navbar-nav .nav-link').forEach(a=>{
    const href = a.getAttribute('href');
    if(href === path){ a.classList.add('active'); }
  });
})();
