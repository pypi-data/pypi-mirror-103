from xml.etree import ElementTree as ET
from xml.dom import minidom
from uuid import uuid4
from os.path import join, dirname
from os import unlink
from json import loads
from __assets__ import assetsCopy, assetsExtract, ARCHICAD_SUPPORT


def readIncludesBySdk(sdk):
    iFile = join(dirname(__file__), 'assets', 'config', 'win',
                 f"includes_{sdk}.json")
    with open(iFile, 'r', encoding='utf-8') as f:
        return loads(f.read(), encoding='utf-8')


def readLibrariesBySdk(sdk):
    lFile = join(dirname(__file__), 'assets', 'config', 'win',
                 f"libraries_{sdk}.json")
    with open(lFile, 'r', encoding='utf-8') as f:
        return loads(f.read(), encoding='utf-8')


def savePrettyXml(xmlRoot,
                  fileName,
                  indent='\t',
                  newline='\n',
                  encoding='utf-8'):
    rawXmlText = ET.tostring(xmlRoot)
    dom = minidom.parseString(rawXmlText)
    with open(fileName, 'w') as doc:
        dom.writexml(doc, '', indent, newline, encoding)


def appendElements(xmlRoot, eles, name, sdk=None):
    if sdk != None:
        ig = ET.SubElement(
            xmlRoot, 'ItemGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})
    else:
        ig = ET.SubElement(xmlRoot, 'ItemGroup')

    for ele in eles:
        flt = ET.SubElement(ig, name, {'Include': ele['Include']})

        if 'Filter' in ele:
            ET.SubElement(flt, 'Filter').text = ele['Filter']

        if 'UniqueIdentifier' in ele:
            ET.SubElement(flt,
                          'UniqueIdentifier').text = ele['UniqueIdentifier']

        if 'Extensions' in ele:
            ET.SubElement(flt, 'Extensions').text = ele['Extensions']


def __init_vcxproj__(base, name, sdks):
    xmlRoot = ET.Element(
        'Project', {
            'DefaultTargets': 'Build',
            'ToolsVersion': '15.0',
            'xmlns': 'http://schemas.microsoft.com/developer/msbuild/2003'
        })

    ig = ET.SubElement(xmlRoot, 'ItemGroup',
                       {'Label': 'ProjectConfigurations'})

    for sdk in sdks:
        pc = ET.SubElement(ig, 'ProjectConfiguration',
                           {'Include': f'{sdk}|x64'})
        ET.SubElement(pc, 'Configuration').text = sdk
        ET.SubElement(pc, 'Platform').text = 'x64'

    ig = ET.SubElement(xmlRoot, 'PropertyGroup', {'Label': 'Globals'})
    ET.SubElement(ig, 'VCProjectVersion').text = '15.0'
    ET.SubElement(ig, 'ProjectGuid').text = f'{uuid4()}'
    ET.SubElement(ig, 'Keyword').text = 'Win32Proj'
    ET.SubElement(ig, 'RootNamespace').text = name
    ET.SubElement(ig, 'WindowsTargetPlatformVersion').text = '10.0.17763.0'

    ET.SubElement(xmlRoot, 'Import',
                  {'Project': R'$(VCTargetsPath)\Microsoft.Cpp.Default.props'})

    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'PropertyGroup', {
                'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'",
                'Label': 'Configuration'
            })
        ET.SubElement(ig, 'ConfigurationType').text = 'DynamicLibrary'
        ET.SubElement(ig, 'UseDebugLibraries').text = 'false'
        ET.SubElement(ig, 'PlatformToolset').text = 'v141'
        ET.SubElement(ig, 'WholeProgramOptimization').text = 'true'
        ET.SubElement(ig, 'CharacterSet').text = 'Unicode'

    ET.SubElement(xmlRoot, 'Import',
                  {'Project': R'$(VCTargetsPath)\Microsoft.Cpp.props'})

    ET.SubElement(xmlRoot, 'ImportGroup', {'Label': 'ExtensionSettings'})

    ET.SubElement(xmlRoot, 'ImportGroup', {'Label': 'Shared'})

    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'ImportGroup', {
                'Label': 'PropertySheets',
                'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"
            })
        ET.SubElement(
            ig, 'Import', {
                'Project':
                R'$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props',
                'Condition':
                R"exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')",
                'Label': 'LocalAppDataPlatform'
            })

    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'PropertyGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})
        ET.SubElement(ig, 'LinkIncremental').text = 'false'
        ET.SubElement(ig, 'TargetExt').text = '.pyd'

        ET.SubElement(
            ig, 'OutDir').text = f'$(SolutionDir)\\release\\{sdk}_module\\'

    for sdk in sdks:
        ig = ET.SubElement(
            xmlRoot, 'ItemDefinitionGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})
        clc = ET.SubElement(ig, 'ClCompile')
        ET.SubElement(clc, 'PrecompiledHeader').text = 'Use'
        ET.SubElement(clc, 'WarningLevel').text = 'Level3'
        ET.SubElement(clc, 'Optimization').text = 'MaxSpeed'
        ET.SubElement(clc, 'FunctionLevelLinking').text = 'true'
        ET.SubElement(clc, 'IntrinsicFunctions').text = 'true'
        ET.SubElement(clc, 'SDLCheck').text = 'true'
        ET.SubElement(
            clc, 'PreprocessorDefinitions'
        ).text = f'NDEBUG;{name.upper()}_EXPORTS;_WINDOWS;_USRDLL;NOMINMAX;PROJECTNAME="{name}";ARCHICAD_{sdk.upper()}=1;%(PreprocessorDefinitions)'
        ET.SubElement(clc, 'ConformanceMode').text = 'true'

        dirs = readIncludesBySdk(sdk)

        ET.SubElement(clc,
                      'AdditionalIncludeDirectories').text = ';'.join(dirs)

        lk = ET.SubElement(ig, 'Link')
        ET.SubElement(lk, 'SubSystem').text = 'Windows'
        ET.SubElement(lk, 'EnableCOMDATFolding').text = 'true'
        ET.SubElement(lk, 'OptimizeReferences').text = 'true'
        ET.SubElement(lk, 'GenerateDebugInformation').text = 'true'
        ET.SubElement(
            lk, 'LinkTimeCodeGeneration').text = 'UseLinkTimeCodeGeneration'

    ig = ET.SubElement(xmlRoot, 'ItemGroup')
    ET.SubElement(ig, 'ClInclude', {'Include': R'src\stdafx.h'})
    ET.SubElement(ig, 'ClInclude', {'Include': R'src\targetver.h'})

    ig = ET.SubElement(xmlRoot, 'ItemGroup')
    ET.SubElement(ig, 'ClCompile', {'Include': R'src\dllmain.cpp'})
    ET.SubElement(ig, 'ClCompile', {'Include': f'src\\{name}.cpp'})
    std = ET.SubElement(ig, 'ClCompile', {'Include': R'src\stdafx.cpp'})

    for sdk in sdks:
        ET.SubElement(
            std, 'PrecompiledHeader', {
                'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"
            }).text = 'Create'

    for sdk in sdks:
        libs = readLibrariesBySdk(sdk)
        appendElements(xmlRoot, libs, 'Library', sdk)

    ET.SubElement(xmlRoot, 'Import',
                  {'Project': R'$(VCTargetsPath)\Microsoft.Cpp.targets'})

    ET.SubElement(xmlRoot, 'ImportGroup', {'Label': 'ExtensionTargets'})

    savePrettyXml(xmlRoot, join(base, f'{name}.vcxproj'))


def __init_vcxproj_user__(base, name, sdks):
    xmlRoot = ET.Element(
        'Project', {
            'ToolsVersion': '15.0',
            'xmlns': 'http://schemas.microsoft.com/developer/msbuild/2003'
        })

    for sdk in sdks:
        if sdk == 'none':
            continue

        ac = sdk.replace("ac", "")
        proGroup = ET.SubElement(
            xmlRoot, 'PropertyGroup',
            {'Condition': f"'$(Configuration)|$(Platform)'=='{sdk}|x64'"})

        ET.SubElement(
            proGroup, 'LocalDebuggerCommand'
        ).text = f'C:\\Program Files\\GRAPHISOFT\\ARCHICAD {ac}\\ARCHICAD.exe'
        ET.SubElement(proGroup, 'DebuggerFlavor').text = 'WindowsLocalDebugger'

    savePrettyXml(xmlRoot, join(base, f'{name}.vcxproj.user'))


def __init_vcxproj_filters__(base, name, sdks):
    filters = [{
        'Include': 'Src',
        'UniqueIdentifier': '{de7d7a13-a071-41e4-8f04-7d1691f7ec83}',
        'Extensions': 'cpp;c;cxx'
    }, {
        'Include': 'Headers',
        'UniqueIdentifier': '{b32da348-770f-41d8-85c9-903e1cc415c5}',
        'Extensions': 'h;hpp;hxx'
    }, {
        'Include': 'Libraries',
        'UniqueIdentifier': '{42902bf0-12fb-4ecb-a6fa-d9d2cf0ceeb9}',
        'Extensions': 'lib'
    }]

    clcs = [{
        'Include': '$(ProjectName).cpp',
        'Filter': 'Src'
    }, {
        'Include': R'src\dllmain.cpp',
        'Filter': 'Src'
    }, {
        'Include': R'src\stdafx.cpp',
        'Filter': 'Src'
    }]

    clis = [{
        'Include': R'src\stdafx.h',
        'Filter': 'Headers'
    }, {
        'Include': R'src\targetver.h',
        'Filter': 'Headers'
    }]

    xmlRoot = ET.Element(
        'Project', {
            'ToolsVersion': '4.0',
            'xmlns': 'http://schemas.microsoft.com/developer/msbuild/2003'
        })

    # ItemGroup Filter
    appendElements(xmlRoot, filters, "Filter")
    appendElements(xmlRoot, clcs, "ClCompile")
    appendElements(xmlRoot, clis, "ClInclude")
    for sdk in sdks:
        libs = readLibrariesBySdk(sdk)
        appendElements(xmlRoot, libs, 'Library', sdk)

    savePrettyXml(xmlRoot, join(base, f'{name}.vcxproj.filters'))


def __modify_entry__(base, name):
    entryHome = join(base, 'src', '__entry__.cpp')
    moduleFile = join(base, 'src', f"{name}.cpp")

    with open(entryHome, 'r', encoding='utf-8') as iFile:
        context = iFile.read()
        context = context.replace("__entry__", name)

    unlink(entryHome)

    with open(moduleFile, 'w', encoding='utf-8') as oFile:
        oFile.write(context)


def initGuide(moduleBase, name, usesdk):
    assetsCopy('module', moduleBase)

    if usesdk:
        sdks = []
        for sdk in ARCHICAD_SUPPORT:
            sdks.append('ac' + str(sdk))
    else:
        sdks = ['none']

    __modify_entry__(moduleBase, name)
    __init_vcxproj__(moduleBase, name, sdks)
    __init_vcxproj_user__(moduleBase, name, sdks)
    __init_vcxproj_filters__(moduleBase, name, sdks)

    libsHome = join(moduleBase, 'libs')
    if usesdk:
        assetsExtract('ac22', libsHome)
        assetsExtract('ac23', libsHome)
        assetsExtract('ac24', libsHome)

    assetsExtract('cast', libsHome)
    assetsExtract('pybind11', libsHome)
    assetsExtract('Python37', libsHome)
