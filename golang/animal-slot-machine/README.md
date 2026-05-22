# 动物老虎机

一个 Go + Vue 编写的模拟老虎/动物机程序。Go 提供随机开奖接口和静态页面服务，Vue 负责投注、滚动动画、赔率展示和开奖记录。

## 运行

```powershell
cd C:\Users\杨威\Desktop\study\2026\golang\animal-slot-machine\frontend
npm install
npm run build

cd ..
go run .
```

启动后访问：

```text
http://localhost:8080
```

## 功能

- 输入投注金额或使用快捷投注按钮。
- 点击动物卡片选择本轮下注动物。
- 点击开始后，动物奖池会持续滚动并逐渐停下。
- Go 后端按权重随机开出大象、老鹰、熊猫等动物。
- 如果开出的动物与下注动物一致，则按该动物赔率返奖；未命中则本轮不中奖。
- 每个动物有不同赔率和中奖概率。
- 页面会展示余额、开奖结果和最近开奖记录。
