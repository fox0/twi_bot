## Структура паттерна

Минимальный паттерн:
```
dev {

}

code {
    act 'stop', 0.5
}
```

todo

В любом месте может быть написано: `act 'действие', вес`

Причём выполнение паттерна продолжится.

Прервать можно так: `return`

Чуть более сложный пример:
```
code {
    import math
    act 'go_left', coord_x

    if 1 == 1 {
        act 'go_right', 0
        return
    }

    act 'go_right', math.sqrt(coord_y)

    function f1() {
        return 1
    }
    act 'stop', f1()
}
```
