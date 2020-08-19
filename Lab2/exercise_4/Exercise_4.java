package exercise_4;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.functions;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.MetadataBuilder;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.graphframes.GraphFrame;
import java.io.IOException;
import java.util.stream.Collectors;
import java.nio.file.Path;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;


public class Exercise_4 {

	private static Row spaceForBeauty(String line){
		String[] item = line.split("\t");
		return RowFactory.create(item[0], item[1]);
	}

	public static void wikipedia(JavaSparkContext ctx, SQLContext sqlCtx) throws IOException {
		Path edges = Paths.get("src/main/resources/wiki-edges.txt");
		Path vertices = Paths.get("src/main/resources/wiki-vertices.txt");

		//Vertices creation
		List<Row> verticesList = Files.lines(vertices).map(s -> spaceForBeauty(s)).collect(Collectors.toList());
		JavaRDD<Row> verticesRDD = ctx.parallelize(verticesList);

		StructType verticesSchema = new StructType(new StructField[]{
				new StructField("id", DataTypes.StringType, true, new MetadataBuilder().build()),
				new StructField("name", DataTypes.StringType, true, new MetadataBuilder().build())
		});
		Dataset<Row> wikiVertices = sqlCtx.createDataFrame(verticesRDD, verticesSchema);

		// Edges Creation
		List<Row> wikiEdgeList = Files.lines(edges).map(s -> spaceForBeauty(s)).collect(Collectors.toList());
		JavaRDD<Row> edgesRDD = ctx.parallelize(wikiEdgeList);

		StructType edgesSchema = new StructType(new StructField[]{
				new StructField("src", DataTypes.StringType, true, new MetadataBuilder().build()),
				new StructField("dst", DataTypes.StringType, true, new MetadataBuilder().build()),
		});
		Dataset<Row> wikiEdges = sqlCtx.createDataFrame(edgesRDD, edgesSchema);
		GraphFrame gf = GraphFrame.apply(wikiVertices, wikiEdges);

		System.out.println(gf);
		gf.edges().show();
		gf.vertices().show();

		// Execute pageRank with d = 0.85 (resetProbability = 1-d) and maxIter = 400
		GraphFrame results = gf.pageRank().resetProbability(0.15).maxIter(10).run();
		Dataset<Row> pageRankNodes =  results.vertices().orderBy(functions.desc("pagerank"));
		// Display top10 pageranks
		pageRankNodes.show(10);
	}

}