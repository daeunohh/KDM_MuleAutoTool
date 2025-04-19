import sys
import os

def make_version_file(version_str: str):
    version_parts = version_str.split(".")
    version_tuple = tuple(map(int, version_parts + ["0"] * (4 - len(version_parts))))

    content = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', 'YourCompany'),
        StringStruct('FileDescription', 'Mule Posting Auto Tool'),
        StringStruct('FileVersion', '{version_str}'),
        StringStruct('InternalName', 'Mule_posting_AutoTool'),
        StringStruct('OriginalFilename', 'Mule_posting_AutoTool_v{version_str}.exe'),
        StringStruct('ProductName', 'Mule Posting Automation'),
        StringStruct('ProductVersion', '{version_str}')])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    with open("version.txt", "w", encoding="utf-8") as f:
        f.write(content)

def build(version_str: str):
    make_version_file(version_str)
    cmd = f'pyinstaller --noconsole --onefile --name=Mule_posting_AutoTool_v{version_str} --version-file=version.txt UI.py'
    os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❗ 사용법: python make_build.py 1.0.3")
    else:
        build(sys.argv[1])
