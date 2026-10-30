/* Navigation accessibility: visual-only improvement; business workflows unchanged. */
document.querySelectorAll("[data-menu]").forEach(function(button){
  var nav=button.closest(".nav")?.querySelector(".links");
  if(!nav)return;
  var id=nav.id||"site-primary-navigation";
  nav.id=id;
  button.setAttribute("aria-controls",id);
  button.setAttribute("aria-expanded",nav.classList.contains("open")?"true":"false");
  button.addEventListener("click",function(){
    var open=nav.classList.toggle("open");
    button.setAttribute("aria-expanded",String(open));
  });
  document.addEventListener("keydown",function(event){
    if(event.key==="Escape"&&nav.classList.contains("open")){
      nav.classList.remove("open");button.setAttribute("aria-expanded","false");button.focus();
    }
  });
  nav.querySelectorAll("a").forEach(function(a){
    a.addEventListener("click",function(){nav.classList.remove("open");button.setAttribute("aria-expanded","false")});
  });
});
document.querySelectorAll("[data-year]").forEach(function(el){el.textContent=new Date().getFullYear()});
