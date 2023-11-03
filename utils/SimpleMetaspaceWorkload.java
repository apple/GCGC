import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Random;

/**
 * A program that simulates a simple metaspace workload.
 *
 * How to run: javac SimpleMetaspaceWorkload.java ; java < gc-algorithm e.g -XX:+UseG1GC > -XX:+PrintGCDetails -Xloggc:< where-to-create/log-file-name e.g ./G1GCMetaspace.log > SimpleMetaspaceWorkload
 */
public class SimpleMetaspaceWorkload {
    public static void main(String[] args) {
        List<Class<?>> classList1 = new ArrayList<>();
        List<Class<?>> classList2 = new ArrayList<>();
        List<Class<?>> classList3 = new ArrayList<>();

        int duration = 550;
        Random random = new Random();

        try {
            for (int j = 0; j < duration; j++) {
                // Names of classes and their corresponding class files that will be loaded
                String class1Name = "SimpleMetaspaceWorkload";
                String class1Code = "SimpleMetaspaceWorkload.class";

                String class2Name = "CustomClassLoader";
                String class2Code = "CustomClassLoader.class";

                String class3Name = "Empty";
                String class3Code = "Empty.class";

                // Create new custom class loaders
                CustomClassLoader customClassLoader1 = new CustomClassLoader();
                CustomClassLoader customClassLoader2 = new CustomClassLoader();
                CustomClassLoader customClassLoader3 = new CustomClassLoader();

                // Load classes
                Class<?> dynamicClass1 = customClassLoader1.defineClass(class1Name, class1Code);
                Class<?> dynamicClass2 = customClassLoader2.defineClass(class2Name, class2Code);
                Class<?> dynamicClass3 = customClassLoader3.defineClass(class3Name, class3Code);

                // Hold the loaded classes in different lists
                classList1.add(dynamicClass1);
                classList2.add(dynamicClass2);
                classList3.add(dynamicClass3);

                int randomInt = random.nextInt(10);

                if (randomInt >= 6) {
                    classList3.clear(); // Remove references to the classes in the list to enable their respective class loaders to be unloaded

                    if (randomInt == 7) {
                        classList2.clear();
                    }

                    if (randomInt == 8) {
                        classList1.clear();
                    }
                }

                System.gc();

                System.out.print(j + 1);
                System.out.print(" of ");
                System.out.println(duration);

                Thread.sleep(450); // Throttle
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class CustomClassLoader extends ClassLoader {
    public Class<?> defineClass(String name, String filePath) throws IOException {
        byte[] bytecode = readClassFile(filePath);
        return defineClass(name, bytecode, 0, bytecode.length);
    }

    private byte[] readClassFile(String filePath) throws IOException {
        return Files.readAllBytes(Paths.get(filePath));
    }
}

class Empty {}
