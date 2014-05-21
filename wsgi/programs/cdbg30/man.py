
import cherrypy

# 這是 MAN 類別的定義
'''
# 在 application 中導入子模組
import programs.cdag30.man as cdag30_man
# 加入 cdag30 模組下的 man.py 且以子模組 man 對應其 MAN() 類別
root.cdag30.man = cdag30_man.MAN()

# 完成設定後, 可以利用
/cdag30/man/assembly
# 呼叫 man.py 中 MAN 類別的 assembly 方法
'''
class MAN(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
這是 2014CDA 協同專案下的 cdag30 模組下的 MAN 類別.<br /><br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="assembly">執行  MAN 類別中的 assembly 方法</a><br /><br />
請確定下列零件於 V:/home/lego/man 目錄中, 且開啟空白 Creo 組立檔案.<br />
<a href="/static/lego_man.7z">lego_man.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />
'''
        return outstring

    @cherrypy.expose
    def assembly(self, *args, **kwargs):
        outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
</head>
<body>
</script><script language="JavaScript">
/*設計一個零件組立函式*/
// featID 為組立件第一個組立零件的編號
// inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
// part2 為外加的零件名稱
function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
ids.Append(featID+inc);
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array(axis1, plane1);
var compDatums = new Array(axis2, plane2);
var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate("pfcComponentConstraints");
    for (var i = 0; i < 2; i++)
    {
        var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var MpfcSelect = pfcCreate ("MpfcSelect");
        var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
        constr.AssemblyReference  = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
        constrs.Append(constr);
    }
asmcomp.SetConstraints(constrs, void null);
}
// 以上為 axis_plane_assembly() 函式
//
function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
ids.Append(featID+inc);
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
}
// 以上為 three_plane_assembly() 函式
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows())
// 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++)
for (var y = 0; y < 4; y++)
{
    if (x == y)
        identityMatrix.Set(x, y, 1.0);
    else
        identityMatrix.Set(x, y, 0.0);
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
throw new Error (0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;

/**---------------------- LEGO_BODY--------------------**/
// 設定零件的 descriptor 物件變數
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName("v:/home/lego/man/LEGO_BODY.prt");
// 若零件在 session 則直接取用
var componentModel = session.GetModelFromDescr(descr);
// 若零件不在 session 則從工作目錄中載入 session
var componentModel = session.RetrieveModel(descr);
// 若零件已經在 session 中則放入組立檔中
if (componentModel != void null)
{
    // 注意這個 asmcomp 即為設定約束條件的本體
    // asmcomp 為特徵物件, 直接將零件, 以 transf 座標轉換矩陣方位放入組立檔案中
    var asmcomp = assembly.AssembleComponent(componentModel, transf);
}

// 建立約束條件變數
var constrs = pfcCreate("pfcComponentConstraints");
// 設定組立檔中的三個定位面, 注意內定名稱與 Pro/E WF 中的 ASM_D_FRONT 不同, 而是 ASM_FRONT, 可在組立件->info->model 中查詢定位面名稱
// 組立檔案中的 Datum 名稱也可以利用 View->plane tag display 查詢名稱
// 建立組立參考面所組成的陣列
var asmDatums = new Array("ASM_FRONT", "ASM_TOP", "ASM_RIGHT");
// 設定零件檔中的三個定位面, 名稱與 Pro/E WF 中相同
var compDatums = new Array("FRONT", "TOP", "RIGHT");
// 建立 ids 變數, intseq 為 sequence of integers 為資料類別, 使用者可以經由整數索引擷取此資料類別的元件, 第一個索引為 0
       // intseq 等同 Python 的數列資料?
var ids = pfcCreate("intseq");
// 利用 assembly 物件模型, 建立路徑變數
var path = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
// 採用互動式設定相關的變數, MpfcSelect 為 Module level class 中的一種
var MpfcSelect = pfcCreate("MpfcSelect");
// 利用迴圈分別約束組立與零件檔中的三個定位平面
for (var i = 0; i < 3; i++)
{
// 設定組立參考面, 也就是 "ASM_FRONT", "ASM_TOP", "ASM_RIGHT" 等三個 datum planes
var asmItem = assembly.GetItemByName (pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
// 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
if (asmItem == void null)
{
    interactFlag = true;
    continue;
}
// 設定零件參考面, 也就是 "FRONT", "TOP", "RIGHT" 等三個 datum planes
var compItem = componentModel.GetItemByName (pfcCreate ("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
// 若無對應的零件參考面, 則啟用互動式平面選擇表單 flag
if (compItem == void null)
{
    interactFlag = true;
    continue;
}
        // 因為 asmItem 為組立件中的定位特徵, 必須透過 path 才能取得
var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, path);
        // 而 compItem 則為零件, 沒有 path 路徑, 因此第二變數為 null
var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        // 利用 ASM_CONSTRAINT_ALIGN 對齊組立約束建立約束變數
var constr = pfcCreate("pfcComponentConstraint").Create (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        // 設定約束條件的組立參考與元件參考選擇
constr.AssemblyReference = asmSel;
constr.ComponentReference = compSel;
       // 第一個變數為強制變數, 第二個為忽略變數
       // 強制變數為 false, 表示不強制約束, 只有透過點與線對齊時需設為 true
       // 忽略變數為 false, 約束條件在更新模型時是否忽略, 設為 false 表示不忽略
       // 通常在組立 closed chain 機構時,  忽略變數必須設為 true, 才能完成約束
       // 因為三個面絕對約束, 因此輸入變數為 false, false
constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
// 將互動選擇相關資料, 附加在程式約束變數之後
constrs.Append(constr);
}

// 設定組立約束條件
asmcomp.SetConstraints (constrs, void null);
/**---------------------- LEGO_ARM_RT 右手上臂--------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/LEGO_ARM_RT.prt");
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
        // 注意這個 asmcomp 即為設定約束條件的本體
        // asmcomp 為特徵物件,直接將零件, 以 transf 座標轉換放入組立檔案中
var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
// 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
// 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
var featID = components.Item(0).Id;

ids.Append(featID);
// 在 assembly 模型中建立子零件所對應的路徑
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
// 以下針對 body 的 A_13 軸與 DTM1 基準面及右臂的  A_4 軸線與 DTM1 進行對齊與面接約束
var asmDatums = new Array("A_13", "DTM1");
var compDatums = new Array("A_4", "DTM1");
// 組立的關係變數為對齊與面接
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
// 組立元件則為軸與平面
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
// 建立約束條件變數, 軸採對齊而基準面則以面接進行約束
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
{
                  // 設定組立參考面, asmItem 為 model item
    var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
                  // 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
                  // 設定零件參考面, compItem 為 model item
    var compItem = componentModel.GetItemByName (relationItem[i], compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
                  // 採用互動式設定相關的變數
    var MpfcSelect = pfcCreate ("MpfcSelect");
    var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
    constr.AssemblyReference  = asmSel;
    constr.ComponentReference = compSel;
                  // 因為透過軸線對齊, 第一 force 變數需設為 true
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
                  // 將互動選擇相關資料, 附加在程式約束變數之後
    constrs.Append(constr);
}
// 設定組立約束條件, 以 asmcomp 特徵進行約束條件設定
// 請注意, 第二個變數必須為 void null 表示零件對零件進行約束, 若為 subPath, 則零件會與原始零件的平面進行約束
asmcomp.SetConstraints (constrs, void null);
/**---------------------- LEGO_ARM_LT 左手上臂--------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/LEGO_ARM_LT.prt");
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
        // 注意這個 asmcomp 即為設定約束條件的本體
        // asmcomp 為特徵物件,直接將零件, 以 transf 座標轉換放入組立檔案中
var asmcomp = assembly.AssembleComponent(componentModel, transf);
}
// 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
var ids = pfcCreate ("intseq");
// 因為左臂也是與 body 進行約束條件組立,  因此取 body 的 featID
// 至此右臂 id 應該是 featID+1, 而左臂則是 featID+2
ids.Append(featID);
// 在 assembly 模型中建立子零件所對應的路徑
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array("A_9", "DTM2");
var compDatums = new Array("A_4", "DTM1");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
// 建立約束條件變數
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
{
                  // 設定組立參考面, asmItem 為 model item
    var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
                  // 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
                  // 設定零件參考面, compItem 為 model item
    var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
                  // 採用互動式設定相關的變數
    var MpfcSelect = pfcCreate ("MpfcSelect");
    var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
    constr.AssemblyReference  = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
                  // 將互動選擇相關資料, 附加在程式約束變數之後
    constrs.Append(constr);
}
// 設定組立約束條件, 以 asmcomp 特徵進行約束條件設定
// 請注意, 第二個變數必須為 void null 表示零件對零件進行約束, 若為 subPath, 則零件會與原始零件的平面進行約束
asmcomp.SetConstraints (constrs, void null);
/**---------------------- LEGO_HAND 右手手腕--------------------**/
// 右手臂 LEGO_ARM_RT.prt 基準  A_2, DTM2
// 右手腕 LEGO_HAND.prt 基準 A_1, DTM3
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/LEGO_HAND.prt");
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
        // 注意這個 asmcomp 即為設定約束條件的本體
        // asmcomp 為特徵物件,直接將零件, 以 transf 座標轉換放入組立檔案中
var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
// 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
var ids = pfcCreate ("intseq");

// 組立件中 LEGO_BODY.prt 編號為 featID
// LEGO_ARM_RT.prt 則是組立件第二個置入的零件,  編號為 featID+1
ids.Append(featID+1);
// 在 assembly 模型中, 根據子零件的編號, 建立子零件所對應的路徑
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
// 以下針對 LEGO_ARM_RT 的 A_2 軸與 DTM2 基準面及 HAND 的  A_1 軸線與 DTM3 進行對齊與面接約束
var asmDatums = new Array("A_2", "DTM2");
var compDatums = new Array("A_1", "DTM3");
// 組立的關係變數為對齊與面接
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
// 組立元件則為軸與平面
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
// 建立約束條件變數, 軸採對齊而基準面則以面接進行約束
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
{
                  // 設定組立參考面, asmItem 為 model item
    var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
                  // 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
                  // 設定零件參考面, compItem 為 model item
    var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
                  // 採用互動式設定相關的變數
    var MpfcSelect = pfcCreate("MpfcSelect");
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
    constr.AssemblyReference  = asmSel;
    constr.ComponentReference = compSel;
                  // 因為透過軸線對齊, 第一 force 變數需設為 true
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
                  // 將互動選擇相關資料, 附加在程式約束變數之後
    constrs.Append(constr);
}
// 設定組立約束條件, 以 asmcomp 特徵進行約束條件設定
// 請注意, 第二個變數必須為 void null 表示零件對零件進行約束, 若為 subPath, 則零件會與原始零件的平面進行約束
asmcomp.SetConstraints (constrs, void null);
// 利用函式呼叫組立左手 HAND
axis_plane_assembly(session, assembly, transf, featID, 2, 
                              "LEGO_HAND.prt", "A_2", "DTM2", "A_1", "DTM3");
// 利用函式呼叫組立人偶頭部 HEAD
// BODY id 為 featID+0, 以 A_2 及  DTM3 約束
// HEAD 則直接呼叫檔案名稱, 以 A_2, DTM2 約束
axis_plane_assembly(session, assembly, transf, featID, 0, 
                              "LEGO_HEAD.prt", "A_2", "DTM3", "A_2", "DTM2");
// Body 與 WAIST 採三個平面約束組立
// Body 組立面為 DTM4, DTM5, DTM6
// WAIST 組立面為 DTM1, DTM2, DTM3
three_plane_assembly(session, assembly, transf, featID, 0, "LEGO_WAIST.prt", "DTM4", "DTM5", "DTM6", "DTM1", "DTM2", "DTM3"); 
// 右腳
axis_plane_assembly(session, assembly, transf, featID, 6, 
                              "LEGO_LEG_RT.prt", "A_8", "DTM4", "A_10", "DTM1");
// 左腳
axis_plane_assembly(session, assembly, transf, featID, 6, 
                              "LEGO_LEG_LT.prt", "A_8", "DTM5", "A_10", "DTM1");
// 紅帽
axis_plane_assembly(session, assembly, transf, featID, 5, 
                              "LEGO_HAT.prt", "A_2", "TOP", "A_2", "FRONT");
// regenerate 並且 repaint 組立檔案
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();    
</script>
</body>
</html>
'''
        return outstring