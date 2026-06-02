# Patrones de Diseño GoF — Gang of Four

> **Autores:** Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides  
> **Obra:** *Design Patterns: Elements of Reusable Object-Oriented Software* (1994)  
> **Materia:** Lenguaje de Programación II — 3er semestre, Ciencia de Datos

Los 23 patrones se agrupan en tres categorías según su propósito:

- **Creacionales (5):** abstraen el proceso de instanciación de objetos.
- **Estructurales (7):** componen clases u objetos en estructuras más grandes.
- **De comportamiento (11):** definen comunicación y responsabilidades entre objetos.

---

## Tabla de patrones

| # | Nombre | Categoría | Problema que resuelve | Diagrama de clases | Casos de uso | Ventajas / Desventajas | Patrones relacionados |
|---|--------|-----------|-----------------------|--------------------|--------------|------------------------|-----------------------|
| 1 | **Abstract Factory** | Creacional | Crear familias de objetos relacionados sin especificar sus clases concretas. | `«interface» AbstractFactory` → `ConcreteFactory1`, `ConcreteFactory2`; cada fábrica crea `AbstractProductA` y `AbstractProductB`. | Kits de UI multiplataforma; acceso a múltiples motores de base de datos; generadores de documentos (PDF/Word). | ✅ Consistencia entre productos; fácil intercambio de familia. ❌ Difícil añadir nuevos tipos de productos; proliferación de clases. | Factory Method, Prototype, Singleton |
| 2 | **Builder** | Creacional | Construir objetos complejos paso a paso separando construcción de representación. | `Director` usa `«interface» Builder`; `ConcreteBuilder` implementa pasos y retorna `Product`. | Constructores de consultas SQL; generadores de XML/HTML; objetos de configuración con muchos parámetros opcionales. | ✅ Control fino del proceso; reutilización del mismo proceso para distintas representaciones. ❌ Requiere crear una clase Builder específica por cada variante. | Abstract Factory, Composite, Prototype |
| 3 | **Factory Method** | Creacional | Definir interfaz para crear un objeto, dejando que las subclases decidan qué clase instanciar. | `Creator` (abstracto) declara `factoryMethod()`; `ConcreteCreator` retorna `ConcreteProduct` que implementa `«interface» Product`. | Frameworks de logging; parsers de distintos formatos; creadores de conexiones según entorno. | ✅ Elimina acoplamiento directo al tipo concreto; respeta Open/Closed. ❌ Puede generar muchas subclases si hay muchos productos. | Abstract Factory, Template Method, Prototype |
| 4 | **Prototype** | Creacional | Crear nuevos objetos clonando instancias existentes en lugar de instanciar desde cero. | `«interface» Prototype` declara `clone()`; `ConcretePrototype1` y `ConcretePrototype2` implementan copia profunda. | Editores gráficos (copiar/pegar); configuraciones predeterminadas; caché de objetos costosos de inicializar. | ✅ Evita clases Factory; reduce coste de inicialización. ❌ Clonar objetos con referencias circulares o recursos externos es complejo. | Abstract Factory, Composite, Decorator, Memento |
| 5 | **Singleton** | Creacional | Garantizar que una clase tenga una única instancia y proporcionar un punto de acceso global. | `Singleton` tiene atributo estático `instancia` y método estático `getInstance()` con constructor privado. | Logger global; configuración de aplicación; pool de conexiones; caché compartido. | ✅ Control garantizado de la instancia única; acceso centralizado. ❌ Dificulta las pruebas unitarias; viola SRP; introduce estado global. | Abstract Factory, Builder, Prototype, Facade |
| 6 | **Adapter** | Estructural | Convertir la interfaz de una clase en otra interfaz que los clientes esperan. | `Client` usa `«interface» Target`; `Adapter` implementa `Target` y delega en `Adaptee` (clase incompatible). | Integración de librerías legadas; adaptadores de formato (XML → JSON); wrappers sobre APIs de terceros. | ✅ Reutiliza clases existentes sin modificarlas; desacopla cliente de implementación. ❌ Aumenta complejidad; puede requerir adaptar muchos métodos. | Bridge, Decorator, Proxy, Facade |
| 7 | **Bridge** | Estructural | Separar la abstracción de su implementación para que ambas puedan variar independientemente. | `Abstraction` contiene referencia a `«interface» Implementor`; `RefinedAbstraction` extiende `Abstraction`; `ConcreteImplementorA/B` implementan `Implementor`. | Drivers de dispositivos; motores de renderizado intercambiables; APIs de GUI multiplataforma. | ✅ Independencia entre abstracción e implementación; extensible en ambas dimensiones. ❌ Mayor complejidad de diseño inicial. | Abstract Factory, Adapter, Strategy |
| 8 | **Composite** | Estructural | Componer objetos en estructuras de árbol y tratar objetos individuales y compuestos uniformemente. | `«interface» Component` implementada por `Leaf` y `Composite`; `Composite` mantiene lista de `Component` hijos. | Sistemas de archivos (archivo vs. carpeta); menús de GUI anidados; expresiones matemáticas; organigramas. | ✅ Trata uniformemente objetos simples y compuestos; facilita agregar nuevos tipos. ❌ Diseño demasiado general; puede dificultar restricciones sobre qué nodos son válidos. | Decorator, Flyweight, Iterator, Visitor |
| 9 | **Decorator** | Estructural | Añadir responsabilidades a objetos dinámicamente sin usar herencia, envolviendo el objeto. | `«interface» Component` ← `ConcreteComponent`; `Decorator` implementa `Component` y contiene referencia a `Component`; `ConcreteDecoratorA/B` extienden `Decorator`. | Streams de I/O (Java); middlewares en Express; validadores encadenados; sistema de permisos acumulables. | ✅ Más flexible que herencia; respeta Open/Closed; combinable. ❌ Muchos objetos pequeños; depuración difícil por múltiples capas. | Adapter, Composite, Strategy, Proxy |
| 10 | **Facade** | Estructural | Proporcionar una interfaz simplificada a un conjunto complejo de interfaces en un subsistema. | `Client` interactúa solo con `Facade`; internamente `Facade` coordina `SubsistemaA`, `SubsistemaB`, `SubsistemaC`. | SDKs de servicios externos; capas de servicio en aplicaciones; interfaces de compiladores; APIs de bibliotecas multimedia. | ✅ Simplifica el uso del subsistema; desacopla al cliente de la complejidad interna. ❌ Puede convertirse en un *god object* que conoce demasiado. | Abstract Factory, Mediator, Singleton |
| 11 | **Flyweight** | Estructural | Usar compartición para soportar eficientemente gran cantidad de objetos de grano fino. | `FlyweightFactory` gestiona pool de `«interface» Flyweight`; `ConcreteFlyweight` comparte estado intrínseco; el estado extrínseco lo pasa el cliente. | Caracteres en procesadores de texto; partículas en motores de videojuegos; íconos repetidos en GUIs. | ✅ Reduce drasticamente el uso de memoria. ❌ Mayor complejidad de código; el estado extrínseco debe gestionarse externamente. | Composite, State, Strategy |
| 12 | **Proxy** | Estructural | Proporcionar un sustituto que controla el acceso a otro objeto. | `Client` usa `«interface» Subject`; `Proxy` y `RealSubject` implementan `Subject`; `Proxy` contiene referencia a `RealSubject`. | Lazy loading de objetos costosos; control de acceso/autorización; caché; logging; objetos remotos (RMI/gRPC). | ✅ Transparente para el cliente; permite control de acceso y optimizaciones. ❌ Introduce indirección; respuesta más lenta; mayor complejidad. | Adapter, Decorator, Facade |
| 13 | **Chain of Responsibility** | Comportamiento | Pasar solicitudes a lo largo de una cadena de manejadores hasta que uno la procese. | `«abstract» Handler` tiene referencia a sucesor (`Handler`) y método `manejar()`; `ConcreteHandler1/2` extienden `Handler` y procesan o delegan. | Middleware HTTP (Express, Django); sistemas de aprobación por niveles; filtros de eventos; manejo de excepciones en capas. | ✅ Desacopla emisor de receptores; fácil añadir/reordenar manejadores. ❌ No garantiza que la solicitud sea atendida; difícil depurar la cadena. | Command, Composite, Decorator |
| 14 | **Command** | Comportamiento | Encapsular una solicitud como objeto para parametrizar, encolar, registrar y soportar deshacer. | `Client` crea `ConcreteCommand` (que implementa `«interface» Command` con `execute()`/`undo()`); `Invoker` lo almacena y ejecuta; `Receiver` realiza la acción. | Undo/Redo en editores; colas de transacciones; macros; sistemas de menús con acciones desacopladas. | ✅ Desacopla emisor de receptor; soporte nativo de undo/redo. ❌ Proliferación de clases Command por cada operación. | Chain of Responsibility, Memento, Observer, Strategy, Prototype |
| 15 | **Interpreter** | Comportamiento | Definir una representación gramatical para un lenguaje y un intérprete para evaluar sentencias. | `«abstract» AbstractExpression` con `interpret(Context)`; `TerminalExpression` y `NonterminalExpression` la implementan; `Context` contiene información global. | Parsers de SQL; expresiones regulares; calculadoras de expresiones; lenguajes de scripting simples. | ✅ Fácil añadir nuevas expresiones; gramática representada explícitamente. ❌ Gramáticas complejas son difíciles de mantener; ineficiente para gramáticas grandes. | Composite, Flyweight, Iterator, Visitor |
| 16 | **Iterator** | Comportamiento | Proporcionar una forma de acceder secuencialmente a elementos de un agregado sin exponer su representación interna. | `«interface» Aggregate` → `ConcreteAggregate`; `«interface» Iterator` (con `next()`, `hasNext()`) → `ConcreteIterator` que referencia `ConcreteAggregate`. | Recorrido de colecciones (listas, árboles, grafos); streams de datos; paginación de resultados. | ✅ Interfaz uniforme para distintas colecciones; múltiples iteradores simultáneos. ❌ Puede ser innecesariamente costoso en colecciones muy simples. | Composite, Memento, Factory Method |
| 17 | **Mediator** | Comportamiento | Definir un objeto que encapsula cómo interactúan un conjunto de objetos, reduciendo dependencias directas. | `«interface» Mediator` ← `ConcreteMediator`; `«abstract» Colleague` referencia `Mediator`; `ConcreteColleague1/2` se comunican solo a través del mediador. | Salas de chat; sistemas de control de tráfico aéreo; formularios con validación cruzada entre campos; event bus. | ✅ Reduce acoplamiento entre colegas; centraliza lógica de coordinación. ❌ El mediador puede volverse muy complejo (*god object*). | Facade, Observer, Command |
| 18 | **Memento** | Comportamiento | Capturar y externalizar el estado interno de un objeto sin violar encapsulamiento, para restaurarlo después. | `Originator` crea y consume `Memento` (estado opaco); `Caretaker` gestiona historial de `Memento` sin acceder a su contenido. | Undo/Redo; snapshots de estado; checkpoints en videojuegos; transacciones reversibles. | ✅ Preserva encapsulamiento; restauración simple. ❌ Alto consumo de memoria si los estados son grandes o frecuentes. | Command, Iterator, Prototype |
| 19 | **Observer** | Comportamiento | Definir dependencia uno-a-muchos para que cuando un objeto cambie, todos sus dependientes sean notificados automáticamente. | `«interface» Subject` (suscribir/notificar) ← `ConcreteSubject`; `«interface» Observer` (actualizar) ← `ConcreteObserver`; `ConcreteSubject` mantiene lista de `Observer`. | Eventos de GUI; patrón MVC (modelo notifica a vistas); sistemas de notificaciones push; pub/sub; reactive streams. | ✅ Acoplamiento débil; soporte broadcast; extensible. ❌ Actualizaciones inesperadas en cascada; orden de notificación no garantizado; difícil depurar. | Mediator, Singleton, Command |
| 20 | **State** | Comportamiento | Permitir que un objeto altere su comportamiento cuando su estado interno cambia, simulando un cambio de clase. | `Context` tiene referencia a `«interface» State`; `ConcreteStateA/B` implementan `State` y pueden cambiar el estado del `Context`. | Máquinas expendedoras; semáforos; estados de un pedido (pendiente/pagado/enviado/entregado); reproductores multimedia. | ✅ Elimina condicionales extensos; organiza código por estado; fácil añadir estados. ❌ Puede generar muchas clases pequeñas para pocos estados simples. | Flyweight, Singleton, Strategy |
| 21 | **Strategy** | Comportamiento | Definir una familia de algoritmos, encapsular cada uno e intercambiarlos en tiempo de ejecución. | `Context` contiene referencia a `«interface» Strategy`; `ConcreteStrategyA/B/C` implementan distintos algoritmos. | Algoritmos de ordenamiento intercambiables; métodos de pago; compresión de archivos; validadores de formulario. | ✅ Elimina condicionales de selección de algoritmo; fácil añadir nuevas estrategias; respeta Open/Closed. ❌ El cliente debe conocer las diferencias entre estrategias. | Bridge, Decorator, State, Template Method |
| 22 | **Template Method** | Comportamiento | Definir el esqueleto de un algoritmo en una clase base, difiriendo pasos específicos a subclases. | `«abstract» AbstractClass` define `templateMethod()` con pasos fijos y métodos abstractos `paso1()`, `paso2()`; `ConcreteClass` implementa los pasos abstractos. | Frameworks de testing (setUp/test/tearDown); parsers de distintos formatos; procesos de autenticación; generadores de reportes. | ✅ Reutilización del esqueleto del algoritmo; control de la estructura. ❌ Limitado a herencia; difícil mantener si el algoritmo tiene muchos pasos variables. | Factory Method, Strategy |
| 23 | **Visitor** | Comportamiento | Separar un algoritmo de la estructura de objetos sobre la que opera, sin modificar los elementos. | `«interface» Visitor` con `visit(ElementoA)`, `visit(ElementoB)` → `ConcreteVisitorA/B`; `«interface» Element` con `accept(Visitor)` → `ConcreteElementA/B`. | Recorrido de AST en compiladores; exportadores de documentos a distintos formatos; reportes sobre estructuras de datos complejas. | ✅ Fácil añadir operaciones nuevas; agrupación lógica de operaciones relacionadas. ❌ Difícil añadir nuevas clases de elemento (requiere modificar todos los Visitor). | Composite, Interpreter, Iterator |

---

## Resumen por categoría

### Creacionales
| Patrón | Intención clave |
|--------|-----------------|
| Abstract Factory | Familias de objetos compatibles |
| Builder | Construcción paso a paso |
| Factory Method | Delegar instanciación a subclases |
| Prototype | Clonar instancias existentes |
| Singleton | Una única instancia global |

### Estructurales
| Patrón | Intención clave |
|--------|-----------------|
| Adapter | Compatibilizar interfaces incompatibles |
| Bridge | Separar abstracción de implementación |
| Composite | Árbol de objetos homogéneo |
| Decorator | Añadir responsabilidades dinámicamente |
| Facade | Simplificar acceso a subsistema |
| Flyweight | Compartir objetos para ahorrar memoria |
| Proxy | Controlar acceso a otro objeto |

### De comportamiento
| Patrón | Intención clave |
|--------|-----------------|
| Chain of Responsibility | Cadena de manejadores |
| Command | Encapsular solicitud como objeto |
| Interpreter | Interpretar sentencias de un lenguaje |
| Iterator | Recorrer colecciones uniformemente |
| Mediator | Centralizar comunicación entre objetos |
| Memento | Capturar y restaurar estado |
| Observer | Notificación uno-a-muchos |
| State | Comportamiento según estado interno |
| Strategy | Algoritmos intercambiables |
| Template Method | Esqueleto de algoritmo con pasos diferidos |
| Visitor | Operaciones sobre estructura de objetos |

---

*Referencia: Gamma, E. et al. (1994). Design Patterns. Addison-Wesley.*
