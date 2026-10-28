# 上传与更新操作手册（零命令行版）

> 目标：把本文件夹上传到 GitHub，开启在线试玩页，并保证**当前试玩版永久留存**。
> 全程在浏览器里点鼠标完成，不需要装 Git。

---

## 第 0 步：先确认你拿到的是这个文件夹

```
github-repo/
├── index.html                     当前 Demo（在线试玩入口）
├── archive/v0.8-trial/index.html  首版试玩版（冻结，永不覆盖）
├── documents/                     策划案 + 数值配表
├── tools/                         仿真与配表生成脚本
├── README.md                      仓库首页展示内容
└── UPLOAD_GUIDE.md                本文件
```

---

## 第 1 步：新建仓库

1. 打开 <https://github.com/new>
2. **Repository name**：`abyss-beast-tamer`（也可用中文名，但英文更稳、链接更干净）
3. **Description**：`单机 Roguelike 爬塔 + 宠物捕获 · 策划案 / 数值配表 / 可玩原型`
4. 可见性：**Public**
   - ⚠️ GitHub 免费账号的 Pages 只能从 **Public** 仓库发布。
   - 代价：**任何人都能下载你的策划案和数值表**。作为求职作品集，公开通常是加分项；若你介意，改为 Private（需 Pro 才能开 Pages），或只公开 Demo、把文档放到私有仓库。
5. **不要**勾选 "Add a README file"（我们自带 README，勾了会冲突）
6. 点 **Create repository**

---

## 第 2 步：上传全部文件

1. 新仓库页面点 **Add file → Upload files**
2. 打开你解压出来的 `github-repo` 文件夹，**全选里面所有内容**（`index.html`、`archive`、`documents`、`tools`、`README.md`、`UPLOAD_GUIDE.md`），拖进网页上传区
   - ⚠️ 拖的是 `github-repo` **里面的东西**，不是 `github-repo` 这个文件夹本身——否则仓库会多出一层无用的目录
   - GitHub 网页上传**支持拖文件夹**，会自动保留子目录结构
3. 等文件列表出现（共 8 个文件），Commit message 填：`v0.8 首版试玩版：Demo + 策划案 + 数值配表`
4. 点 **Commit changes**

**校验**：仓库首页应能看到 `index.html`、`archive/`、`documents/`、`tools/` 四项，README 自动显示在下方。

---

## 第 3 步：开启在线试玩（GitHub Pages）

1. 仓库页 → **Settings**（顶部菜单）
2. 左侧栏 → **Pages**
3. **Source** 选 `Deploy from a branch`
4. **Branch** 选 `main`，目录选 `/ (root)` → 点 **Save**
5. 等 **1–3 分钟**，刷新本页，顶部会出现：
   `Your site is live at https://<你的用户名>.github.io/abyss-beast-tamer/`

**这个链接就是试玩地址**，手机电脑都能开。

> 若显示 404：① 确认 Branch 是 `main`、目录是 `/ (root)`；② 再等 2–5 分钟（首次构建较慢）；③ 确认仓库是 Public。

---

## 第 4 步：冻结 v0.8（双保险，防止旧版丢失）

**保险一：archive 目录（已内置，不用操作）**
`archive/v0.8-trial/index.html` 是首版试玩版的独立副本。以后你更新根目录 `index.html`，这个文件**不会被动**，旧版永久可玩：
`https://<你的用户名>.github.io/abyss-beast-tamer/archive/v0.8-trial/`

**保险二：打 Release（网页操作，1 分钟）**

1. 仓库页 → 右侧 **Releases** → **Create a new release**
2. **Choose a tag** 输入 `v0.8-trial` → 点 "Create new tag on publish"
3. **Release title**：`v0.8 首版试玩版`
4. **Describe**：`8 层垂直切片 + 1 Boss；节点系统 / 捕获 / 战斗闭环跑通`
5. 点 **Publish release**

之后每次大版本都这样打一个 Release，GitHub 会保留每个版本的源码快照 + 一键下载 zip，**任何旧版本都不会丢**。

---

## 第 5 步：以后更新新版（关键：别覆盖 archive）

做完 24 层或新一轮迭代后：

1. 仓库页 → **Add file → Upload files**
2. 只把**新的 `index.html`** 拖进去（同名会自动覆盖）
3. Commit message 填：`v0.9 24 层完整版`
4. 到 Releases 再打一个 `v0.9`
5. **不要动** `archive/` 下任何文件

这样：在线玩的是最新版，`archive/` 保留历史存档，Releases 保留全量快照，三重保险。

---

## 可选：用命令行上传（更稳，能保留完整提交历史）

如果以后想更专业地管理版本，在本机装 Git 后在 `github-repo` 目录执行：

```bash
git init
git add .
git commit -m "v0.8 首版试玩版：Demo + 策划案 + 数值配表"
git branch -M main
git remote add origin https://github.com/<你的用户名>/abyss-beast-tamer.git
git push -u origin main
```

> 推送时 GitHub 要求使用 **Personal Access Token**（不是账号密码）。
> 生成入口：Settings → Developer settings → Personal access tokens → Fine-grained tokens，权限只勾该仓库的 `Contents: Read and write`，有效期设 7 天。
> ⚠️ **Token 等同于密码，不要发给任何人，也不要粘贴到聊天窗口里。**

---

## 常见问题

| 问题 | 解法 |
|---|---|
| 页面打开是 README 而不是游戏 | Pages 的 Branch/目录没设对，选 `main` + `/ (root)` |
| 中文文件名显示成乱码 | 一般不影响；若出现，把文档改成英文名 `design-doc-v0.8.docx` |
| 上传时提示文件过大 | 单文件上限 25MB（网页上传），本项目最大 450KB，不会触发 |
| 手机上玩布局挤 | 当前按 PC 宽屏设计，属已知缺口，非 bug |
| 声音不出来 | 浏览器策略：先点一次「开始游戏」 |
| 想撤销某次上传 | 仓库页 → Commits → 找到那次 → Revert |
