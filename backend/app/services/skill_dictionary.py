"""
Central skill dictionary used by both
resume parsing and JD parsing.

Canonical skill -> list of variants
"""

SKILL_MAP = {
    # Frontend
    "react": ["react", "reactjs", "react.js"],
    "redux": ["redux", "redux toolkit"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "html": ["html"],
    "css": ["css"],
    "vue": ["vue", "vuejs", "vue.js"],
    "angular": ["angular", "angularjs"],
    "jquery": ["jquery"],
    "graphql": ["graphql"],

    # Backend
    "java": ["java"],
    "spring boot": ["spring boot", "springboot"],
    "spring": ["spring framework"],
    "spring mvc": ["spring mvc"],
    "jpa": ["jpa", "java persistence api"],
    "hibernate": ["hibernate", "jpa/hibernate"],
    "python": ["python"],
    "node.js": ["node", "node.js", "nodejs"],
    "express": ["express", "express.js"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "c++": ["c++", "cpp","C++"],
    "c#": ["c#", "csharp", "c sharp"],
    "c": ["c programming"],
    "go": ["go", "golang"],
    "rust": ["rust"],
    "php": ["php"],
    "ruby": ["ruby"],
    "ruby on rails": ["ruby on rails", "rails"],
    "kotlin": ["kotlin"],
    "scala": ["scala"],
    "swift": ["swift"],
    "r": ["r programming"],
    "perl": ["perl"],
    "bash": ["bash", "shell scripting", "shell"],
    "powershell": ["powershell"],

    # Databases & ORM
    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "cassandra": ["cassandra"],
    "dynamodb": ["dynamodb"],
    "elasticsearch": ["elasticsearch"],
    "redis": ["redis"],
    "memcached": ["memcached"],
    "firebase": ["firebase"],

    # API & Web Services
    "rest api": ["rest api", "rest apis", "rest"],
    "soap": ["soap"],
    "oauth": ["oauth"],
    "jwt": ["jwt", "json web token"],
    "api gateway": ["api gateway"],

    # Messaging / Caching
    "kafka": ["kafka", "apache kafka"],
    "rabbitmq": ["rabbitmq"],
    "activemq": ["activemq"],

    # DevOps / Cloud / Servers
    "docker": ["docker", "dockerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "openshift": ["openshift", "red hat openshift"],
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud"],
    "azure": ["azure"],
    "nginx": ["nginx"],
    "apache": ["apache"],
    "tomcat": ["tomcat", "apache tomcat"],
    "jboss": ["jboss", "wildfly", "wildfly/jboss"],
    "jenkins": ["jenkins"],
    "teamcity": ["teamcity"],
    "gitlab ci": ["gitlab ci"],
    "github actions": ["github actions"],
    "terraform": ["terraform"],
    "ansible": ["ansible"],
    "puppet": ["puppet"],
    "chef": ["chef"],

    # Build Tools
    "maven": ["maven"],
    "gradle": ["gradle"],
    "npm": ["npm"],
    "yarn": ["yarn"],
    "webpack": ["webpack"],
    "gulp": ["gulp"],

    # Testing
    "junit": ["junit"],
    "testng": ["testng"],
    "pytest": ["pytest"],
    "mocha": ["mocha"],
    "jest": ["jest"],
    "selenium": ["selenium"],
    "cypress": ["cypress"],

    # Core Concepts
    "data structures": ["data structures", "data structures and algorithms"],
    "algorithms": ["algorithms", "data structures and algorithms"],
    "object oriented design": ["object oriented design", "ood", "oop"],
    "system design": ["system design"],

    # Tools & Others
    "git": ["git", "github", "gitlab"],
    "linux": ["linux"],
    "windows": ["windows"],
    "macos": ["macos", "mac"],
    "jira": ["jira"],
    "confluence": ["confluence"],
    "gerrit": ["gerrit"],
    "svn": ["svn", "subversion"],
    "hg": ["hg", "mercurial"],
}
