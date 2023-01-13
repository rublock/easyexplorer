let balanceToggle = document.querySelector('.balanceToggle');
let btcBalance = document.querySelector('.btcBalance');
let usdBalance = document.querySelector('.usdBalance');

balanceToggle.addEventListener("click", () => {
    if (usdBalance.classList.contains('hide')) {
        btcBalance.classList.toggle('hide')
        usdBalance.classList.toggle('hide')
    } else {
        btcBalance.classList.toggle('hide')
        usdBalance.classList.toggle('hide')
    }
})