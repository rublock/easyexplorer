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
    console.log('Welcome to btcblockexplorer.io!')
}

//LOAD ANIMATION

document.querySelectorAll(".page").forEach(e => e.addEventListener("click", function () {
    document.querySelector(".loader_wrapper").style.display = 'flex';
}))

document.querySelector(".loader_wrapper").style.display = 'none';