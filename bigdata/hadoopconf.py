#!/usr/bin/env python

# This file's configuration is only for

from tempfile import NamedTemporaryFile

def write_core_temp(master_ip):
    f = NamedTemporaryFile(mode='w+t')
    # /opt/bitnami/hadoop/etc/hadoop/core-site.xml
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
    <name>fs.default.name</name>
    <value>hdfs://{}:9000</value>
  </property>
  <property>
      <name>dfs.http.address</name>
      <value>50070</value>
  </property>
  <property>
      <name>hadoop.tmp.dir</name>
      <value>/opt/bitnami/hadoop/var/lib</value>
  </property>
  <property>
    <name>hadoop.proxyuser.hadoop.hosts</name>
    <value>*</value>
  </property>
  <property>
    <name>hadoop.proxyuser.hadoop.groups</name>
    <value>*</value>
  </property>
  <property>
    <name>hadoop.proxyuser.root.hosts</name>
    <value>*</value>
  </property>
  <property>
    <name>hadoop.proxyuser.root.groups</name>
    <value>*</value>
  </property>
</configuration>""".format(master_ip))

    f.seek(0)
    f.close()


def write_hdfs_temp():
    f = NamedTemporaryFile(mode='w+t')
    # /opt/bitnami/hadoop/etc/hadoop/hdfs-site.xml
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
</configuration>""")
    f.name
    f.close()


def write_mapred_temp():
    f = NamedTemporaryFile(mode='w+t')
    # /opt/bitnami/hadoop/etc/hadoop/mapred-site.xml
    f.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
</configuration>""")
    f.name
    f.close()


def write_yarn_temp(yarn_resource_ip):
    f = NamedTemporaryFile(mode='w+t')
    # /opt/bitnami/hadoop/etc/hadoop/yarn-site.xml
    f.write("""<?xml version="1.0"?>
<configuration>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Site specific YARN configuration properties -->

<!--
  <property>
      <name>yarn.resourcemanager.webapp.address</name>
      <value>8088</value>
  </property>
-->
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>{}</value>
  </property>

  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
  <property>
    <name>yarn.nodemanager.remote-app-log-dir</name>
    <value>/opt/bitnami/hadoop/logs</value>
  </property>
  <property>
    <name>yarn.nodemanager.remote-app-log-dir-suffix</name>
    <value>remote</value>
  </property>
</configuration>""".format(yarn_resource_ip))
    f.name
    f.close()

if __name__ == '__main__':
    write_core_temp()
