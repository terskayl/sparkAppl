function App() {
    const [data, setData] = React.useState({
        posts : [],
        toFetch : 'add',
    })

    React.useEffect(() => {
        fetch(data.toFetch, {method: 'GET',})
            .then(response => response.json())
            .then(postsList => setData({
                ...data,
                posts: postsList,
            }))
    }, [data.toFetch])

    return (<div>
        <CreateForm />
        {data.posts.map(post => <Post key={post.id} id={post.id} author={post.author} body={post.body} liked_by={post.liked_by} viewer={post.viewer} pfp={post.pfp} comments={post.comments} images={post.images} />)}
    </div>);
}

function Pfp(props) {
    return (
        <img className='rounded-full w-full' src={props.pfp} alt={props.username}/>
    );
}
function UserInfo(props) {
    return (
        <div className='flex flex-row py-2'>
            <div className='w-8'>
                <Pfp username={props.username} pfp={props.pfp ? props.pfp : 'https://static.thenounproject.com/png/193196-200.png' } />
            </div>
            <div className='tracking-wide px-2 pt-1 align-bottom'>
                {props.username}
            </div>
        </div>
    );
}
function Post(props) {

    const [state, setState] = React.useState({
        liked : props.liked_by.indexOf(props.viewer) > -1,
        viewer : props.viewer,
        id : props.id,
        likes : props.liked_by.length
    })
    function likeToggle() {
        fetch('posts', {
            method: 'PUT',
            body: JSON.stringify({
                liked: !state.liked,
                viewer: state.viewer,
                id: state.id
            })
        })
        setState({
            ...state,
            likes: state.likes += state.liked ? -1 : 1,
            liked: !state.liked
        })
    }


    return (
        <div className="relative bg-slate-100 px-6 pt-10 pb-8 my-8 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:max-w-lg sm:rounded-lg sm:px-10">
            <UserInfo username={props.author} pfp={props.pfp} />
            <div>
                <img className='rounded border border-slate-200 w-full'
                     src={props.images.length > 0 ? props.images[0] : "https://static.vecteezy.com/system/resources/previews/005/337/799/original/icon-image-not-found-free-vector.jpg"}
                     alt=""/>
            </div>
            {props.body ? (<div className='pb-2'>
                <span className='font-normal'> {props.author} </span> <span className='font-light'> {props.body} </span>
                <br/> <br/> <span className='font-light text-gray-400'></span>
            </div>) : (<div></div>) }
            <div className='py-2' onClick={likeToggle}>
                <button>
                    <span className={state.liked ? 'bi-heart-fill' : 'bi-heart'}></span>
                </button>
                <span className='pl-2'>{state.likes} {state.likes === 1 ? 'like' : 'likes'} </span>
            </div>
            <div className=' text-gray-400 font-light'>
                {props.comments.length} comments
            </div>
            <div className='pb-2'>
                {props.comments.map(comment => <div> <span>{comment[0]} </span> <span className='font-light pl-2'>{comment[1]}</span> </div>)}
            </div>
            <form action="comments" method="POST">
                <div className='flex'>
                    <div className='w-full'>
                        <input type='hidden' name='postId' value={props.id}/>
                        <input className='w-full py-1 px-2 rounded' placeholder='Add a comment...' name='body' type="text"/>
                    </div>
                    <div className='w-12 px-2 py-1'>
                        <button type="submit">Post</button>
                    </div>
                </div>
            </form>
        </div>
    );
}

function CreateForm(props) {
    const [state, setState] = React.useState({
        images : []
    })

    function addPic(event) {
        event.preventDefault();
        setState({
            images : state.images.concat([event.target[0].value])
        })
    }

    return (
        <div className="relative bg-white px-4 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:max-w-lg sm:rounded-lg sm:px-4">
            <h1 className='text-xl font-bold tracking-wider p-4 text-center'>Create New Post</h1>
            <div>Images:</div>
            <div className='w-full bg-gray-200 grid grid-cols-3 gap-2 p-2'>
                {state.images.map(image => (<div className='col-span-1'>
                    <img src={image} alt=""
                         className='w-full h-full rounded-xl object-cover'/>
                </div>))}
            </div>
            <div>
                <form onSubmit={addPic}>
                    <input type="url" className='border rounded'/>
                    <button type="submit" className="px-2 py-1 bg-teal-500 text-white" >Add Image URL</button>
                </form>
                <form action='add' method="POST">
                    <input type="hidden" name="images" value={state.images[0]}/>
                    <textarea name="body" id="body" className='w-full h-24'
                              placeholder="Write description here!"></textarea>
                    <button type="submit" data-modal-hide="Modal"
                            className='text-white bg-teal-500 py-2 px-2 rounded font-bold tracking-widest'>POST
                    </button>
                </form>
            </div>
        </div>
    )
}

ReactDOM.render(<App />, document.querySelector("#post"));

