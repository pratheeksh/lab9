import java.io.IOException;
import java.util.*;
import java.util.regex.*;
import java.util.Map.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;
import org.apache.hadoop.mapred.SequenceFileOutputFormat;

public class TweetCount {

    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
	private final static IntWritable one = new IntWritable(1);
	private Text word = new Text();

	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
	    String line = value.toString();
	    StringTokenizer tokenizer = new StringTokenizer(line);
	    Pattern p = Pattern.compile( "#(\\w+|\\W+)");
	    while (tokenizer.hasMoreTokens()) {
		String t = tokenizer.nextToken();
		Matcher m = p.matcher(t);
		boolean b = m.matches();

		if( b ){ 
		    word.set(t);
		    context.write(word, one);
		}
	    }
	}
    } 	




    public static class Reduce extends Reducer<Text, IntWritable,Text , IntWritable> {

	//private java.util.SortedMap<Text,Integer> top = new TreeMap<Text,Integer>();
	private java.util.Map<Text,Integer> countMap = new HashMap<Text,Integer>();

	@Override
	    public void reduce(Text key, Iterable<IntWritable> values, Context context) 
	    throws IOException, InterruptedException {
		int s = 0;
		for (IntWritable val : values) {
		    s+= val.get();

		}

		IntWritable sum = new IntWritable();
		countMap.put(new Text(key), s);

	    }
	@Override
	    protected void cleanup(Context context) throws IOException, InterruptedException {
		java.util.Map <Text, Integer>top = sortByValues(countMap); 
		int counter = 0;
		for (Entry< Text, Integer> entry : top.entrySet()){
		    if (counter <50){
			context.write(new Text(entry.getKey()), new IntWritable(entry.getValue()));
		    }
		    else{break;}
		    counter++;


		}
	    }


    }
    public static <K extends Comparable,V extends Comparable> java.util.Map<K,V> sortByValues(java.util.Map<K,V> map){
	List<Entry<K,V>> entries = new LinkedList<Entry<K,V>>(map.entrySet());

	Collections.sort(entries, new Comparator<Entry<K,V>>() {

		@Override
		public int compare(Entry<K, V> o1, Entry<K, V> o2) {
		return o2.getValue().compareTo(o1.getValue());
		}
		});
	java.util.Map<K,V> sortedMap = new LinkedHashMap<K,V>();

	for(Entry<K,V> entry: entries){
	    sortedMap.put(entry.getKey(), entry.getValue());
	}

	return sortedMap;
    }


    public static void main(String[] args) throws Exception {
	Configuration conf = new Configuration();
	Job job = new Job(conf, "TweetCount");


	job.setMapperClass(Map.class);
	job.setReducerClass(Reduce.class);
	job.setOutputFormatClass(TextOutputFormat.class);
	job.setInputFormatClass(TextInputFormat.class);
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(IntWritable.class);   



	job.setNumReduceTasks(1);
	job.setJarByClass(TweetCount.class);

	FileInputFormat.addInputPath(job, new Path(args[0]));
	FileOutputFormat.setOutputPath(job, new Path(args[1]));

	job.waitForCompletion(true);



    }
}

