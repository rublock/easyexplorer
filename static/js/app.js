let balanceToggle = document.querySelector('.balanceToggle');
let btcBalance = document.querySelector('.btcBalance');
let usdBalance = document.querySelector('.usdBalance');

try {
    balanceToggle.addEventListener("click", () => {
        if (usdBalance.classList.contains('hide')) {
            btcBalance.classList.toggle('hide')
            usdBalance.classList.toggle('hide')
        } else {
            btcBalance.classList.toggle('hide')
            usdBalance.classList.toggle('hide')
        }
    })
} catch {
    console.log('Welcome to easyExplorer.io!')
}

