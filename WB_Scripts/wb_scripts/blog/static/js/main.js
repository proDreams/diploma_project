function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

const csrftoken = getCookie('csrftoken');

const switchTheme = async (color) => {

    const res = await fetch(``, {

        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify({color}),
        credentials: 'same-origin',

    });
}

document.getElementById('btnSwitch').addEventListener('click', () => {
    if (document.documentElement.getAttribute('data-bs-theme') === 'dark') {
        document.documentElement.setAttribute('data-bs-theme', 'light');
        switchTheme('light').then();
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        switchTheme('dark').then();
    }
})


let copyList = document.querySelectorAll('.copy-clipboard');
let copyArray = Array.prototype.slice.call(copyList);

function tooltipUpdate(button, tooltip, title) {
    tooltip.dispose();
    button.setAttribute('title', title);
    tooltip = new bootstrap.Tooltip(button);
    tooltip.show();

    return tooltip;
}

copyArray.map(function (copy) {
    let text = copy.querySelector('code').innerText;
    let button = copy.querySelector('button');
    let tooltip = new bootstrap.Tooltip(button);

    button.addEventListener('mouseover', function () {
        tooltip = tooltipUpdate(button, tooltip, 'Скопировать');
    });

    button.addEventListener('click', function () {
        window.navigator.clipboard.writeText(text);
        tooltip = tooltipUpdate(button, tooltip, 'Готово!');
    });
});