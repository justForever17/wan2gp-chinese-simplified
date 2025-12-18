# Wan2GP Chinese Localization Plugin (HanHua)

这是一个为 **Wan2GP** (Wan-To-Generate-Pixel) 视频生成工具提供的中文汉化插件。

由于 Wan2GP 的界面是基于 Gradio 动态生成的，单纯的插件无法覆盖所有文本，因此本仓库包含了一个**修改版的核心文件 (`wgp.py`)** 以及**汉化插件本体**。

## 包含文件

- `wgp.py`: 修改后的主程序文件，修复了进度条显示问题，并增加了对汉化插件的底层支持。
- `plugins/Chinese-Simplified/`: 汉化插件文件夹，包含插件代码和翻译字典。
- `plugins/wan2gp-plugin-manager/`: **修复版**插件管理器，解决了插件列表无法显示的问题。

## 安装说明

1.  **备份原文件**:
    在使用本插件前，请先备份您 Wan2GP 根目录下的 `wgp.py` 文件。

2.  **替换主程序**:
    将本仓库中的 `wgp.py` 文件复制到您的 Wan2GP 根目录，覆盖原文件。
    *注意：此修改版 `wgp.py` 修复了原版进度条不更新的 Bug，并增强了 UI 组件的访问权限以支持汉化。*

3.  **安装插件**:
    将 `plugins` 文件夹下的汉化插件复制到您的 Wan2GP 的 `plugins/` 目录中。
    建议同时覆盖 `wan2gp-plugin-manager` 里的 `plugin.py` 以修复插件管理界面可能为空白的问题。
    安装后的路径结构应如下所示：
    ```text
    Wan2GP/
    ├── wgp.py
    ├── plugins/
    │   ├── Chinese-Simplified/
    │   │   ├── ...
    │   ├── wan2gp-plugin-manager/  <-- (推荐更新)
    │   │   └── plugin.py
    │   └── ...
    ```

4.  **运行**:
    正常启动 Wan2GP：
    ```bash
    python wgp.py
    ```
    启动后，界面（包括侧边栏、下拉菜单和提示信息）应自动显示为简体中文。

## 如何自行维护汉化

本插件使用基于字典的翻译机制。如果发现有新的英文内容未被汉化，或者想修改现有的翻译，可以按照以下步骤操作：

### 1. 识别未汉化内容 (Localization logging)

修改版的插件内置了未翻译内容的检测功能。
在运行 Wan2GP 的终端（Console）窗口中，留意以 `[Localization]` 开头的日志信息。

一旦插件遇到字典中不存在的文本，它会输出类似以下的警告：
```text
[Localization] Missing translation for: 'New English Feature'
```

### 2. 添加翻译

打开 `plugins/Chinese-Simplified/translations.json` 文件（推荐使用 VS Code 或 Notepad++ 等支持 JSON 格式的编辑器）。

在 JSON 对象中添加新的键值对：
```json
{
    "Existing Text": "现有文本",
    "New English Feature": "新功能的中文翻译"
}
```
*注意：请确保 JSON 格式正确（最后一项不要加逗号，使用双引号）。*

### 3. 生效

修改 `translations.json` 后，**必须重启 Wan2GP** 才能使新的翻译生效。

## 关闭日志信息

默认情况下，插件会在控制台输出未找到翻译的文本，以便于完善汉化。如果您觉得这些日志太吵，可以通过设置环境变量来关闭它：

*   **Powershell**: `$env:WAN2GP_I18N_DEBUG="False"`
*   **CMD**: `set WAN2GP_I18N_DEBUG=False`

或者直接修改 `plugins/Chinese-Simplified/plugin.py` 文件，在 `translate_text` 函数中找到相关判断逻辑进行调整。

## 贡献

如果您完善了 `translations.json`，欢迎提交 Pull Request 或分享您的翻译文件给社区！
