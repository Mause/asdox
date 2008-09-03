import stringtemplate3,os,sys
from asdox import asBuilder,asModel

builder = asBuilder.Builder()
builder.addSource("C:\\Projects\\RAD\\as3\\vo")

#[Table(name,options,createOptions,constraints)]
#[Column(name,type,typeConstraints,length,options,constraints)]
class Column:
    def __init__(self):
        self.name = ""
        self.type = ""
        self.typeConstraints = ""
        self.size = ""
        self.options = ""
        self.constraints = ""
class Table:
    def __init__(self):
        self.name = ""
        self.options = ""
        self.createOptions = ""
        self.constraints = ""
        self.keys = []
        self.nonkeys = []
        self.columns = []

initMap = {'Boolean':'false','int':'0','Number':'0','String':'""','unit':'0','Date':'NULL'}
pdoMap = {'Boolean':',PDO::PARAM_BOOL','int':',PDO::PARAM_INT','Number':'','String':',PDO::PARAM_STR','unit':',PDO::PARAM_INT','Date':''}
mysqlMap = {'Boolean':'tinyint','int':'int','Number':'decimal','String':'varchar','unit':'int','Date':'Date'}
for pkg in builder.packages.values():
    for cls in pkg.classes.values():
        
        template = stringtemplate3.StringTemplate("""
<?
public class $table.object$DAO
{
        public function get(\$vo)
        {
        	\$sth = \$dbh->prepare('SELECT $table.columns:{ col |$col.name$};separator=","$ FROM $table.object$ WHERE $table.keys:{ col |$col.name$ = :$col.name$};separator=","$')
                $table.keys:{ col |\$sth->bindParam(':$col.name$',\$vo->$col.object$);};separator=","$
                
        	\$sth->execute();
                var \$results = \$sth->fetchAll();
                \$dbh = null;
                return \$results;
        }
        
        public function save(&\$vo)
        {
        	if( $table.keys:{ col |\$vo->$col.name$ == 0};separator=" && "$ )
                {
                	\$this->insert(\$vo);
                }
                else
                {
                	\$this->update(\$vo);
                }
        }
        
        private function insert(&\$vo)
        {
        	\$sth = \$dbh->prepare('INSERT INTO $table.object$ ($table.nonkeys:{ col |$col.name$};separator=","$) VALUES($table.nonkeys:{ col |:$col.name$};separator=","$)')
        	$table.nonkeys:{ col |\$sth->bindParam(':$col.name$',\$vo->$col.object$);};separator="\n"$
        	\$sth->execute();
        }
        
        private function update(&\$vo)
        {
        	\$sth = \$dbh->prepare('UPDATE $table.object$ SET $table.nonkeys:{ col |\$$col.name$ = :$col.name$};separator=","$ WHERE $table.keys:{ col |$col.name$ = :$col.name$};separator=","$ ')
                $table.nonkeys:{ col |\$sth->bindParam(':$col.name$',\$vo->$col.object$);};separator="\n"$
                $table.keys:{ col |\$sth->bindParam(':$col.name$',\$vo->$col.object$);};separator="\n"$
        	\$sth->execute();
                \$dbh = null;
        }
        
        public function delete(\$vo)
        {
        	\$sth = \$dbh->prepare('DELETE FROM $table.object$ WHERE $table.keys:{ col |$col.name$ = :$col.name$};separator=" AND "$')
                $table.keys:{ col |\$sth->bindParam(':$col.name$',\$vo->$col.object$);};separator="\n"$
        	\$sth->execute();
                \$dbh = null;
        }
        
        public function create(\$vo)
        {
        	\$sth = \$dbh->prepare('CREATE TABLE $table.object$ ($table.columns:{ col |$col.name$ $col.type$$col.size$ $col.typeConstraints$ $col.options$};separator=","$) $table.options$')
        }
}
?>
        """)
        tbl = Table()
        tbl.object = cls.name

        for prop in cls.variables.values():
            if prop.visibility == "public" and prop.type in initMap:
                for meta in prop.metadata:
                    if meta.name == "Column":
                        col = Column()
                        if "name" in meta.params:
                            col.name = meta.params["name"]
                        else:
                            col.name = prop.name
                        if "type" in meta.params:
                            if meta.params["type"] in mysqlMap:
                                col.type = mysqlMap[meta.params["type"]]
                            else:
                                col.type = meta.params["type"]
                        else:
                            if prop.type in mysqlMap:
                                col.type = mysqlMap[prop.type]
                            else:
                                col.type = prop.type
                        if "length" in meta.params:
                            col.size = "(" + meta.params["length"] + ")"
                        if prop.isProperty and prop.readable:
                            col.object = "get" + prop.name.capitalize() + "()"
                        else:
                            col.object = prop.name
                        options = []
                        if "options" in meta.params:
                            options = meta.params["options"].split(",")
                        if "PRIMARY KEY" in options:
                            tbl.keys.append(col)
                        else:
                            tbl.nonkeys.append(col)
        tbl.columns.extend(tbl.keys)
        tbl.columns.extend(tbl.nonkeys)
        
        template["table"] = tbl
        print str(template)
