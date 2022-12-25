
var bmi_tooltip = document.querySelector('.bmi-tooltip')
var bmi_progress = document.querySelector('.bmi-progress')

// set width cho thanh bmi bar dựa trên bmi của user
var bmi = bmi_tooltip.getAttribute('data-bmi')
bmi_progress_percent = (bmi / 40) * 100
if(bmi_progress_percent > 1) bmi_progress_percent = 100
bmi_progress.style.width =  bmi_progress_percent + '%'
bmi_tooltip.innerHTML = bmi
