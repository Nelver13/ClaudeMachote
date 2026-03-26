# Skill: WinForms (VB / C#)
name: winforms
description: Convenciones para proyectos de escritorio con WinForms en Visual Basic o C#. Se activa al trabajar con .sln, .vbproj, .csproj o formularios de escritorio.
allowed tools: Read, Grep, Glob, Edit, Write

---

## Convenciones

- Lógica de negocio separada de la UI — nunca en code-behind del formulario
- Conexión a DB encapsulada en capa de datos (`DataAccess/`)
- Nombres de formularios: `Frm[Nombre]` (ej: `FrmUsuarios`)
- Prefijos de controles: `btn`, `txt`, `lbl`, `dgv`, `cmb`, `chk`, `pnl`
- Strings de conexión en `App.config` — nunca hardcodeados

## Estructura del proyecto

```
[Proyecto]/
├── Forms/
│   └── FrmNombre.vb / .cs
├── Models/
│   └── NombreModel.vb / .cs
├── DataAccess/
│   └── NombreDA.vb / .cs
├── Services/
│   └── NombreService.vb / .cs
└── App.config
```

## Patrones

### String de conexión (App.config)
```xml
<connectionStrings>
  <add name="DBPrincipal"
       connectionString="Server=.;Database=MiDB;Integrated Security=True;"
       providerName="System.Data.SqlClient" />
</connectionStrings>
```

### Capa de datos (VB)
```vb
' ARCHIVO: NombreDA.vb
' QUÉ HACE: acceso a datos para [entidad]
Public Class NombreDA
    Private connStr As String = ConfigurationManager.ConnectionStrings("DBPrincipal").ConnectionString

    Public Function ObtenerTodos() As DataTable
        ' implementación
    End Function
End Class
```

### Capa de datos (C#)
```csharp
// ARCHIVO: NombreDA.cs
// QUÉ HACE: acceso a datos para [entidad]
public class NombreDA
{
    private string connStr = ConfigurationManager.ConnectionStrings["DBPrincipal"].ConnectionString;

    public DataTable ObtenerTodos()
    {
        // implementación
    }
}
```

## Antes de arrancar

1. Verificar versión de .NET Framework objetivo
2. Identificar motor de DB (SQL Server, SQLite, Access)
3. Verificar si usa ORM (Entity Framework) o ADO.NET directo
